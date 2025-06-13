"""
Message handlers for the Telegram bot.
"""

import re
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from ..config import LANGUAGES, MESSAGES
from ..services.state import state_manager
from ..services.piston import piston_service, PistonAPIError
from ..utils.logger import get_logger
from ..utils.helpers import handle_errors, RateLimiter, check_channel_membership, send_channel_membership_message
from ..config import Config

logger = get_logger(__name__)

# Rate limiter instance
rate_limiter = RateLimiter(
    max_requests=Config.RATE_LIMIT_MAX_REQUESTS,
    window_seconds=Config.RATE_LIMIT_WINDOW
)


@handle_errors("Sorry, an error occurred while processing your message.")
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages."""
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user_code = update.message.text
    
    # Update user activity
    state_manager.update_user_activity(user_id)
    
    # Check channel membership (only for private chats)
    if not await check_channel_membership(update, context):
        await send_channel_membership_message(update)
        return
    
    # Check if user has selected a language
    user_language = state_manager.get_user_language(chat_id)
    if user_language:
        await execute_user_code(update, context, user_code, user_language)
    else:
        # Only send language selection message in private chats, ignore in groups
        if update.message.chat.type == "private":
            await update.message.reply_text(MESSAGES["select_language_first"], parse_mode="Markdown")


async def handle_return_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle return button press."""
    chat_id = update.message.chat_id
    
    # Clear user's language selection
    state_manager.clear_user_language(chat_id)
    
    # Only show keyboard buttons in private chats, not in groups
    reply_markup = None
    if update.message.chat.type == "private":
        # Show language selection buttons again
        keyboard = [
            [
                KeyboardButton("🐍 Python"),
                KeyboardButton("💻 C++"),
                KeyboardButton("📚 C#"),
            ],
            [KeyboardButton("🐚 Bash"), KeyboardButton("🦄 Go"), KeyboardButton("🖥 C")],
            [
                KeyboardButton("🧠 Brainfuck"),
                KeyboardButton("🖥 JavaScript"),
                KeyboardButton("🧑‍💻 PHP"),
            ],
            [KeyboardButton("🦀 Rust"), KeyboardButton("☕️ Java")],
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        MESSAGES["exit_code_mode"],
        reply_markup=reply_markup
    )


async def execute_user_code(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                           code: str, language: str) -> None:
    """Execute user's code."""
    user_id = update.message.from_user.id
    
    # Rate limiting check
    if not rate_limiter.is_allowed(str(user_id)):
        await update.message.reply_text(MESSAGES["rate_limited"])
        return
    
    try:
        logger.info(f"Executing {language} code for user {user_id}")
        
        # Execute code
        code_output = await piston_service.execute_code(code, language)
        
        # Send output
        output_message = MESSAGES["output_prefix"].format(output=code_output)
        await update.message.reply_text(output_message, parse_mode="Markdown")
        
        logger.info(f"Code execution completed for user {user_id}")
        
    except PistonAPIError as e:
        logger.error(f"Piston API error for user {user_id}: {e}")
        error_message = MESSAGES["error_executing"].format(error=str(e))
        await update.message.reply_text(error_message)
    
    except Exception as e:
        logger.error(f"Unexpected error executing code for user {user_id}: {e}")
        await update.message.reply_text(MESSAGES["service_unavailable"])


@handle_errors("Sorry, an error occurred while processing the run command.")
async def handle_run_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /run command with inline code."""
    user_id = update.message.from_user.id
    message_text = update.message.text
    
    # Update user activity
    state_manager.update_user_activity(user_id)
    
    # Check channel membership (only for private chats)
    if not await check_channel_membership(update, context):
        await send_channel_membership_message(update)
        return
    
    # Rate limiting check
    if not rate_limiter.is_allowed(str(user_id)):
        await update.message.reply_text(MESSAGES["rate_limited"])
        return
    
    # Match the pattern /run or /run@<bot_username> followed by the language and code
    match = re.match(r"^/run(?:@\w+)?\s+(\w+)\s+([\s\S]+)", message_text)
    
    if match:
        language = match.group(1).lower()
        user_code = match.group(2).strip()
        
        try:
            logger.info(f"Executing {language} code via /run command for user {user_id}")
            
            # Execute code
            code_output = await piston_service.execute_code(user_code, language)
            
            # Send output
            output_message = MESSAGES["output_prefix"].format(output=code_output)
            await update.message.reply_text(output_message, parse_mode="Markdown")
            
            logger.info(f"Code execution via /run completed for user {user_id}")
            
        except PistonAPIError as e:
            logger.error(f"Piston API error for user {user_id}: {e}")
            error_message = MESSAGES["error_executing"].format(error=str(e))
            await update.message.reply_text(error_message)
        
        except Exception as e:
            logger.error(f"Unexpected error executing code for user {user_id}: {e}")
            await update.message.reply_text(MESSAGES["service_unavailable"])
    
    else:
        # Show improved usage instructions
        help_text = (
            "🚀 **How to Use iRunCode Bot**\n\n"
            "**📝 Command Format:**\n"
            "`/run <language_name>`\n"
            "`Your code here (can be multiple lines)`\n\n"
            "**🔍 Examples:**\n\n"
            "**Python:**\n"
            "```\n"
            "/run python\n"
            "print('Hello, World!')\n"
            "for i in range(3):\n"
            "    print(f'Count: {i}')\n"
            "```\n\n"
            "**JavaScript:**\n"
            "```\n"
            "/run javascript\n"
            "console.log('Hello, World!');\n"
            "const nums = [1, 2, 3];\n"
            "console.log(nums.map(x => x * 2));\n"
            "```\n\n"
            "**C++:**\n"
            "```\n"
            "/run cpp\n"
            "#include <iostream>\n"
            "int main() {\n"
            "    std::cout << \"Hello, World!\" << std::endl;\n"
            "    return 0;\n"
            "}\n"
            "```\n\n"
            "**🌟 Popular Languages:**\n"
            "• `python` - Python 3.10\n"
            "• `javascript` - JavaScript\n"
            "• `java` - Java 15\n"
            "• `cpp` - C++ 10.2\n"
            "• `csharp` - C# 10.0\n"
            "• `go` - Go 1.16\n"
            "• `rust` - Rust 1.68\n"
            "• `php` - PHP 8.2\n\n"
            "**💡 Pro Tips:**\n"
            "• Language names are case-sensitive\n"
            "• Multi-line code is fully supported\n"
            "• Use `/langs` to see all supported languages\n"
            "• Use `/help` for more detailed information\n"
            "• Most standard libraries are available\n\n"
            "**⚡ Quick Start:** Just type `/run python` then your Python code!"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")


@handle_errors("Sorry, an error occurred while processing your selection.")
async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language button press."""
    user_id = update.message.from_user.id
    selected_language = update.message.text
    
    # Update user activity
    state_manager.update_user_activity(user_id)
    
    # Check channel membership (only for private chats)
    if not await check_channel_membership(update, context):
        await send_channel_membership_message(update)
        return
    
    # Add debug logging
    logger.info(f"User {user_id} pressed button: '{selected_language}'")
    
    # Handle special buttons first
    if selected_language == "👾 Other Languages":
        logger.info("Other Languages button pressed - calling other_languages_info")
        from .commands import other_languages_info
        await other_languages_info(update, context)
        return
    elif selected_language == "↪️ Return":
        await handle_return_button(update, context)
        return
    
    # Handle regular language buttons
    logger.info(f"Available languages: {list(LANGUAGES.keys())}")
    
    if selected_language in LANGUAGES:
        language = LANGUAGES[selected_language]
        logger.info(f"Language selected: {language}")
        await enter_code_mode(update, context, language)
    else:
        logger.warning(f"Invalid language button pressed: '{selected_language}'")
        await update.message.reply_text(MESSAGES["invalid_language"], parse_mode="Markdown")


async def enter_code_mode(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                         language: str) -> None:
    """Enter code input mode for selected language."""
    chat_id = update.message.chat_id
    
    # Set user's selected language
    state_manager.set_user_language(chat_id, language)
    
    # Only show return button in private chats, not in groups
    reply_markup = None
    if update.message.chat.type == "private":
        # Display "Return" button to exit code input mode
        keyboard = [[KeyboardButton("↪️ Return")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    message = MESSAGES["language_selected"].format(language=language)
    await update.message.reply_text(message, reply_markup=reply_markup)
