"""
Command handlers for the Telegram bot.
"""

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from ..config import LANGUAGES, SUPPORTED_LANGUAGES_TEXT, MESSAGES
from ..services.state import state_manager
from ..utils.logger import get_logger
from ..utils.helpers import handle_errors

logger = get_logger(__name__)


@handle_errors("Sorry, an error occurred while processing your request.")
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    
    logger.info(f"User {user_id} ({user_name}) started the bot")
    
    # Update user activity
    state_manager.update_user_activity(user_id)
    
    # Create keyboard with language options
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
        [KeyboardButton("👾 Other Languages")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_message = MESSAGES["welcome"].format(name=user_name)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


@handle_errors("Sorry, an error occurred while processing the help command.")
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} requested help")
    
    state_manager.update_user_activity(user_id)
    
    help_text = (
        "🚀 *How to Use the Bot*:\n\n"
        "1️⃣ Use the `/run` command followed by the language name and your code.\n\n"
        "📝 *Command Format*:\n"
        "`/run <language_name>`\n"
        "`Your code here`\n\n"
        "🔍 *Example (Python)*:\n"
        "`/run python`\n"
        '`print("Hello, World!")`\n\n'
        f"📚 *Supported Languages*:\n"
        f"`{SUPPORTED_LANGUAGES_TEXT}`\n\n"
        "💡 *Tip*: Make sure to enter the command and code in the exact format for it to work!"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


@handle_errors("Sorry, an error occurred while processing the about command.")
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command."""
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} requested about info")
    
    state_manager.update_user_activity(user_id)
    
    about_text = (
        "Hi👋, Thanks for using my bot\\. \n"
        "This is an open\\-source project and the source code can be found "
        "[here](https://github\\.com/meower1/)\\. The bot is built using "
        "[python\\-telegram\\-bot](https://python\\-telegram\\-bot\\.org/) in Python\\. "
        "And it uses the [Piston API](https://github\\.com/engineer\\-man/piston) "
        "to run code snippets\\. \n\n"
        "If you have any questions or suggestions, feel free to reach out to me on "
        "[Telegram](https://t\\.me/meow3r)\\.\n"
        "And also checkout my [My Channel](https://t\\.me/area51_blog)\n"
        "Have fun coding\!💫"
    )
    
    await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN_V2)


@handle_errors("Sorry, an error occurred while processing the languages command.")
async def supported_languages_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /langs command."""
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} requested supported languages")
    
    state_manager.update_user_activity(user_id)
    
    langs_text = f"📚 *Supported Languages*:\n`{SUPPORTED_LANGUAGES_TEXT}`\n\n"
    await update.message.reply_text(langs_text, parse_mode="Markdown")


@handle_errors("Sorry, an error occurred while processing other languages info.")
async def other_languages_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle other languages button press."""
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} requested other languages info")
    
    state_manager.update_user_activity(user_id)
    
    help_text = (
        "🚀 *How to Use the Bot*:\n\n"
        "1️⃣ Use the `/run` command followed by the language name and your code.\n\n"
        "📝 *Command Format*:\n"
        "`/run <language_name>`\n"
        "`Your code here`\n\n"
        "🔍 *Example (Python)*:\n"
        "`/run python`\n"
        '`print("Hello, World!")`\n\n'
        f"📚 *Supported Languages*:\n"
        f"`{SUPPORTED_LANGUAGES_TEXT}`\n\n"
        "💡 *Tip*: Make sure to enter the command and code in the exact format for it to work!"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")
