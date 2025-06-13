"""
Main application entry point.
"""

import asyncio
import re
import signal
import sys
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from .config import Config
from .utils.logger import setup_logging, get_logger
from .utils.health import health_monitor, graceful_shutdown
from .handlers.commands import (
    start_command,
    help_command,
    about_command,
    supported_languages_command,
)
from .handlers.messages import (
    handle_message,
    handle_run_command,
    handle_button_press,
)
from .utils.helpers import handle_membership_check_callback
from .config import LANGUAGES

# Initialize logging
logger = setup_logging()


class TelegramBot:
    """Main Telegram bot class."""
    
    def __init__(self):
        self.application = None
        self.health_task = None
    
    async def setup_application(self):
        """Set up the Telegram application."""
        # Validate configuration
        Config.validate()
        
        # Create application with better configuration
        self.application = (
            ApplicationBuilder()
            .token(Config.API_KEY)
            .concurrent_updates(True)
            .connection_pool_size(Config.CONNECTION_POOL_SIZE)
            .pool_timeout(Config.POOLING_TIMEOUT)
            .read_timeout(Config.BOT_TIMEOUT)
            .write_timeout(Config.BOT_TIMEOUT)
            .build()
        )
        
        # Add command handlers
        self.application.add_handler(CommandHandler("start", start_command))
        self.application.add_handler(CommandHandler("help", help_command))
        self.application.add_handler(CommandHandler("about", about_command))
        self.application.add_handler(CommandHandler("langs", supported_languages_command))
        self.application.add_handler(CommandHandler("run", handle_run_command))
        
        # Add callback query handler for membership check
        self.application.add_handler(CallbackQueryHandler(handle_membership_check_callback, pattern="check_membership"))
        
        # Add message handlers
        # Handle language buttons and other special buttons (only in private chats)
        language_patterns = list(LANGUAGES.keys()) + ["👾 Other Languages", "↪️ Return"]
        self.application.add_handler(
            MessageHandler(
                filters.TEXT & filters.Regex("|".join(re.escape(pattern) for pattern in language_patterns)) & filters.ChatType.PRIVATE,
                handle_button_press,
            )
        )
        
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        )
        
        # Add error handler
        self.application.add_error_handler(self._error_handler)
        
        logger.info("Telegram application configured successfully")
    
    async def _error_handler(self, update, context):
        """Handle errors."""
        logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)
    
    async def start(self):
        """Start the bot."""
        try:
            logger.info("Starting iRunCode Telegram Bot...")
            
            # Setup application
            await self.setup_application()
            
            # Start health monitoring
            self.health_task = asyncio.create_task(health_monitor.start_monitoring())
            
            # Initialize the application
            await self.application.initialize()
            await self.application.start()
            
            # Start polling
            await self.application.updater.start_polling(
                allowed_updates=["message", "callback_query"],
                drop_pending_updates=True
            )
            
            logger.info("Bot started successfully!")
            
            # Keep the bot running
            while not graceful_shutdown.shutdown_requested:
                await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise
    
    async def stop(self):
        """Stop the bot."""
        logger.info("Stopping bot...")
        
        try:
            # Stop health monitoring
            if self.health_task:
                health_monitor.stop_monitoring()
                self.health_task.cancel()
                try:
                    await self.health_task
                except asyncio.CancelledError:
                    pass
            
            # Stop the application
            if self.application:
                await self.application.updater.stop()
                await graceful_shutdown.shutdown(self.application)
            
            logger.info("Bot stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")


def setup_signal_handlers(bot):
    """Setup signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        graceful_shutdown.shutdown_requested = True
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


async def main():
    """Main entry point."""
    bot = TelegramBot()
    
    # Setup signal handlers
    setup_signal_handlers(bot)
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        await bot.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
