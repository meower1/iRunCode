"""
Utilities for error handling and decorators.
"""

import asyncio
import functools
import time
from typing import Any, Callable, Dict, Optional
from collections import defaultdict, deque

from ..utils.logger import get_logger

# Import Telegram types (will only work when telegram library is installed)
try:
    from telegram import Update, ChatMember, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import ContextTypes
    from telegram.error import TelegramError
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

logger = get_logger(__name__)

# Import Telegram types - these will be available when the bot runs
try:
    from telegram import Update, ChatMember
    from telegram.ext import ContextTypes
    from telegram.error import TelegramError
except ImportError:
    # Handle import errors during development/testing
    Update = None
    ChatMember = None
    ContextTypes = None
    TelegramError = Exception


class RateLimiter:
    """Simple rate limiter implementation."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)
    
    def is_allowed(self, user_id: str) -> bool:
        """Check if request is allowed for user."""
        now = time.time()
        user_requests = self.requests[user_id]
        
        # Remove old requests outside the window
        while user_requests and user_requests[0] < now - self.window_seconds:
            user_requests.popleft()
        
        # Check if under limit
        if len(user_requests) < self.max_requests:
            user_requests.append(now)
            return True
        
        return False


def retry_async(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator for retrying async functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier for delay
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}"
                    )
                    
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            
            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        
        return wrapper
    return decorator


def handle_errors(default_response: Optional[str] = None):
    """
    Decorator for handling errors in handler functions.
    
    Args:
        default_response: Default response to send on error
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                
                # Try to send error message to user if possible
                if default_response and len(args) >= 1:
                    try:
                        update = args[0]
                        if hasattr(update, 'message') and hasattr(update.message, 'reply_text'):
                            await update.message.reply_text(default_response)
                    except Exception as reply_error:
                        logger.error(f"Failed to send error response: {reply_error}")
        
        return wrapper
    return decorator


def sanitize_code_output(output: str, max_length: int = 4000) -> str:
    """
    Sanitize code output for Telegram message.
    
    Args:
        output: Raw output from code execution
        max_length: Maximum length of output
    
    Returns:
        Sanitized output string
    """
    if not output:
        return "No output"
    
    # Remove null bytes and other problematic characters
    output = output.replace('\x00', '').replace('\r\n', '\n').replace('\r', '\n')
    
    # Truncate if too long
    if len(output) > max_length:
        output = output[:max_length] + "\n\n... (output truncated)"
    
    # Escape markdown special characters
    output = output.replace('`', '\\`').replace('*', '\\*').replace('_', '\\_')
    
    return output


def format_exception(e: Exception) -> str:
    """Format exception for user-friendly display."""
    return f"{type(e).__name__}: {str(e)}"


async def check_channel_membership(update, context) -> bool:
    """
    Check if user is a member of the required channel.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    
    Returns:
        True if user is a member or if check is disabled/not applicable, False otherwise
    """
    if not TELEGRAM_AVAILABLE:
        return True
    
    # Import Config here to avoid circular imports
    from ..config import Config
    
    # Skip check if feature is disabled
    if not Config.REQUIRE_CHANNEL_MEMBERSHIP:
        return True
    
    # Skip check if this is a group chat (only apply to private chats)
    if update.message.chat.type != "private":
        return True
    
    user_id = update.message.from_user.id
    
    try:
        # Get chat member info
        member = await context.bot.get_chat_member(
            chat_id=Config.REQUIRED_CHANNEL_ID,
            user_id=user_id
        )
        
        logger.info(f"Checking membership for user {user_id} in channel {Config.REQUIRED_CHANNEL_ID}")
        logger.info(f"Member status: {member.status}")
        
        # Check if user is a member (including creator, administrator, member)
        # Use string comparison for better compatibility across library versions
        allowed_statuses = ["creator", "owner", "administrator", "member"]
        
        is_member = member.status in allowed_statuses
        
        if not is_member:
            logger.info(f"User {user_id} is not a member of required channel {Config.REQUIRED_CHANNEL_ID} (status: {member.status})")
        else:
            logger.info(f"User {user_id} is a member of required channel {Config.REQUIRED_CHANNEL_ID}")
        
        return is_member
    
    except TelegramError as e:
        # If we can't check membership (e.g., channel doesn't exist, bot not in channel)
        # Log the error but allow the user to proceed to avoid breaking the bot
        logger.error(f"Failed to check channel membership for user {user_id}: {e}")
        return True
    
    except Exception as e:
        logger.error(f"Unexpected error checking channel membership for user {user_id}: {e}")
        return True


async def send_channel_membership_message(update) -> None:
    """Send a message asking user to join the required channel with an interactive button."""
    if not TELEGRAM_AVAILABLE:
        return
    
    # Import Config here to avoid circular imports
    from ..config import Config
    
    channel_id = Config.REQUIRED_CHANNEL_ID
    channel_link = channel_id
    
    # If it's a username (starts with @), convert to a clickable link
    if channel_link.startswith('@'):
        channel_link = f"https://t.me/{channel_link[1:]}"
    
    # Make the channel ID a clickable link by using markdown link format
    message = (
        "🔒 **Channel Membership Required**\n\n"
        f"To use this bot, please join our channel first:\n"
        f"👉 [{channel_id}]({channel_link})\n\n"
        f"After joining, try using the bot again!"
    )
    
    # Create an inline keyboard with a glass-style join button
    keyboard = [
        [InlineKeyboardButton("🪐 Join Channel", url=channel_link)],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_membership")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        message, 
        parse_mode="Markdown", 
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


async def handle_membership_check_callback(update, context) -> None:
    """Handle the 'I've Joined' button callback."""
    if not TELEGRAM_AVAILABLE:
        return
    
    query = update.callback_query
    await query.answer()
    
    # Check if user is now a member
    # Create a mock update object for the membership check
    class MockMessage:
        def __init__(self, chat, from_user):
            self.chat = chat
            self.from_user = from_user
    
    class MockUpdate:
        def __init__(self, message):
            self.message = message
    
    # Create mock objects to reuse the existing check function
    mock_update = MockUpdate(MockMessage(query.message.chat, query.from_user))
    
    is_member = await check_channel_membership(mock_update, context)
    
    if is_member:
        # User is now a member, show success message
        await query.edit_message_text(
            "✅ **Great! You've joined the channel!**\n\n"
            "You can now use the bot. Type /start to begin!",
            parse_mode="Markdown"
        )
    else:
        # User is still not a member
        await query.edit_message_text(
            "❌ **Not Joined Yet**\n\n"
            "Please make sure you've joined the channel and try again.\n"
            "Click the button below to join:",
            parse_mode="Markdown",
            reply_markup=update.callback_query.message.reply_markup
        )
