"""
Command handlers for the Telegram bot.
"""

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from ..config import LANGUAGES, SUPPORTED_LANGUAGES_TEXT, MESSAGES, LANGUAGE_CATEGORIES, USAGE_EXAMPLES
from ..services.state import state_manager
from ..utils.logger import get_logger
from ..utils.helpers import handle_errors, check_channel_membership, send_channel_membership_message

logger = get_logger(__name__)


@handle_errors("Sorry, an error occurred while processing your request.")
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    
    logger.info(f"User {user_id} ({user_name}) started the bot")
    
    # Update user activity
    state_manager.update_user_activity(user_id)
    
    # Check channel membership (only for private chats)
    if not await check_channel_membership(update, context):
        await send_channel_membership_message(update)
        return
    
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
        "🚀 *iRunCode Bot - Help Guide*\n\n"
        "🔧 *Commands:*\n"
        "• `/start` - Start the bot and show language selection\n"
        "• `/help` - Show this help message\n"
        "• `/about` - Information about the bot\n"
        "• `/langs` - Quick list of popular languages\n"
        "• `/run <language>` followed by your code\n\n"
        "📝 *How to Run Code:*\n"
        "1️⃣ Method 1: Use language buttons\n"
        "   • Click a language button (🐍 Python, etc.)\n"
        "   • Send your code\n"
        "   • Get results!\n\n"
        "2️⃣ Method 2: Use `/run` command\n"
        "   • Type: `/run <language_name>`\n"
        "   • Send your code on next line(s)\n"
        "   • Example:\n"
        "   ```\n"
        "   /run python\n"
        "   print('Hello, World!')\n"
        "   for i in range(3):\n"
        "       print(f'Number: {i}')\n"
        "   ```\n\n"
        "🌟 *Special Features:*\n"
        "• Click '👾 Other Languages' for 50+ languages with examples\n"
        "• Organized by categories (Popular, Web, Systems, etc.)\n"
        "• Usage examples for each language type\n"
        "• Multi-line code support\n"
        "• Fast and secure execution\n\n"
        "💡 *Pro Tips:*\n"
        "• Language names are case-sensitive\n"
        "• Most standard libraries are available\n"
        "• Code execution is limited to 30 seconds\n"
        "• Rate limited: 10 requests per minute\n\n"
        "Happy coding! 🎉"
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
        "Have fun coding!💫"
    )
    
    await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN_V2)


@handle_errors("Sorry, an error occurred while processing the languages command.")
async def supported_languages_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /langs command with organized language listing."""
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} requested supported languages")
    
    state_manager.update_user_activity(user_id)
    
    # Check channel membership (only for private chats)
    if not await check_channel_membership(update, context):
        await send_channel_membership_message(update)
        return
    
    # Import the new language categories
    from ..config import LANGUAGE_CATEGORIES
    
    response_parts = []
    response_parts.append("📚 *Supported Programming Languages*")
    response_parts.append("=" * 35)
    response_parts.append("")
    
    # Count total languages
    total_languages = sum(len(languages) for languages in LANGUAGE_CATEGORIES.values())
    response_parts.append(f"🎯 *Total: {total_languages}+ languages supported!*")
    response_parts.append("")
    
    # Quick reference for popular languages
    popular_langs = [
        "🐍 `python` - Python", "🟨 `javascript` - JavaScript", "☕ `java` - Java",
        "💻 `cpp` - C++", "📚 `csharp` - C#", "🦄 `go` - Go", 
        "🦀 `rust` - Rust", "🧑‍💻 `php` - PHP", "💎 `ruby` - Ruby"
    ]
    
    response_parts.append("🔥 *Most Popular:*")
    for lang in popular_langs:
        response_parts.append(f"  {lang}")
    response_parts.append("")
    
    # Quick usage
    response_parts.append("📝 *Quick Usage:*")
    response_parts.append("```")
    response_parts.append("/run python")
    response_parts.append("print('Hello, World!')")
    response_parts.append("```")
    response_parts.append("")
    
    response_parts.append("💡 *Tips:*")
    response_parts.append("• Use exact language names (case-sensitive)")
    response_parts.append("• Click '👾 Other Languages' for full categorized list")
    response_parts.append("• Multi-line code is supported")
    response_parts.append("• Most standard libraries are available")
    response_parts.append("")
    
    response_parts.append("🚀 *More Commands:*")
    response_parts.append("• `/help` - Show detailed help")
    response_parts.append("• `/about` - About this bot")
    response_parts.append("• Click '👾 Other Languages' for complete list with examples")
    
    full_response = "\n".join(response_parts)
    await update.message.reply_text(full_response, parse_mode="Markdown")


@handle_errors("Sorry, an error occurred while processing other languages info.")
async def other_languages_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle other languages button press with comprehensive language information."""
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} requested other languages info")
    
    state_manager.update_user_activity(user_id)
    
    # Check channel membership (only for private chats)
    if not await check_channel_membership(update, context):
        await send_channel_membership_message(update)
        return
    
    # Import the new language categories
    from ..config import LANGUAGE_CATEGORIES, USAGE_EXAMPLES
    
    # Create a comprehensive response with categories
    response_parts = []
    
    # Header
    response_parts.append("🚀 *iRunCode - All Supported Languages*")
    response_parts.append("=" * 40)
    response_parts.append("")
    
    # Add quick usage instructions
    response_parts.append("📝 *How to Use:*")
    response_parts.append("• `/run <language> <your_code>`")
    response_parts.append("• Example: `/run python print('Hello!')`")
    response_parts.append("")
    
    # Add languages by category
    for category, languages in LANGUAGE_CATEGORIES.items():
        response_parts.append(f"{category}")
        response_parts.append("─" * 25)
        
        for lang_code, lang_name, emoji in languages:
            response_parts.append(f"{emoji} `{lang_code}` - {lang_name}")
        
        response_parts.append("")
    
    # Add some popular examples
    response_parts.append("💡 *Popular Examples:*")
    response_parts.append("")
    
    # Python example
    response_parts.append("🐍 *Python:*")
    response_parts.append("```python")
    response_parts.append("/run python")
    response_parts.append("print('Hello, World!')")
    response_parts.append("for i in range(3):")
    response_parts.append("    print(f'Count: {i}')")
    response_parts.append("```")
    response_parts.append("")
    
    # JavaScript example
    response_parts.append("🟨 *JavaScript:*") 
    response_parts.append("```javascript")
    response_parts.append("/run javascript")
    response_parts.append("console.log('Hello, World!');")
    response_parts.append("const numbers = [1, 2, 3];")
    response_parts.append("console.log(numbers.map(x => x * 2));")
    response_parts.append("```")
    response_parts.append("")
    
    # Fun esoteric example
    response_parts.append("🧠 *Brainfuck (for fun):*")
    response_parts.append("```brainfuck")
    response_parts.append("/run brainfuck")
    response_parts.append("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.")
    response_parts.append("```")
    response_parts.append("*(Prints 'Hello World!')*")
    response_parts.append("")
    
    # Additional tips
    response_parts.append("� *Pro Tips:*")
    response_parts.append("• Use exact language names from the list")
    response_parts.append("• Multi-line code works perfectly")
    response_parts.append("• Most languages support standard libraries")
    response_parts.append("• Check `/help` for more commands")
    response_parts.append("")
    response_parts.append("Happy coding! 🎉")
    
    # Join all parts
    full_response = "\n".join(response_parts)
    
    # Split into chunks if too long (Telegram has a 4096 character limit)
    max_length = 4000
    if len(full_response) <= max_length:
        await update.message.reply_text(full_response, parse_mode="Markdown")
    else:
        # Split into multiple messages
        chunks = []
        current_chunk = []
        current_length = 0
        
        for line in response_parts:
            line_length = len(line) + 1  # +1 for newline
            if current_length + line_length > max_length and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = [line]
                current_length = line_length
            else:
                current_chunk.append(line)
                current_length += line_length
        
        if current_chunk:
            chunks.append("\n".join(current_chunk))
        
        # Send each chunk
        for i, chunk in enumerate(chunks):
            if i == 0:
                await update.message.reply_text(chunk, parse_mode="Markdown")
            else:
                await update.message.reply_text(f"*Continued...*\n\n{chunk}", parse_mode="Markdown")
