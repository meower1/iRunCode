import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from piston import execute_code
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.info("Starting bot...")

# Dictionary to track the state of users (language selected)
user_language_state = {}

# Define supported languages
LANGUAGES = {
    "🐍 Python": "python",
    "💻 C++": "cpp",
    "📚 C#": "csharp",
    "🐚 Bash": "bash",
    "🦄 Go": "go",
    "🖥 C": "c",
    "🧠 Brainfuck": "brainfuck",
    "🖥 JavaScript": "javascript",
    "🧑‍💻 PHP": "php",
    "🦀 Rust": "rust",
    "☕️ Java": "java",
}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        f"Hello {update.message.from_user.first_name}. Select a language to run your code:",
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Use the buttons to select a programming language, then input your code. Press 'Return' to exit code input mode."
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
        Hi, Thanks for using my bot. This is an opensource project and the source code can be found [here](https://github.com/meower1/)
        The bot is built using [python-telegram-bot](https://python-telegram-bot.org/) in python
        And it uses the [Piston API](https://github.com/engineer-man/piston) to run code snippets.

        If you have any questions or suggestions, feel free to reach out to me on [Telegram](https://t.me/meow3r)
        """
    )


async def run_code_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE, language: str
) -> None:
    chat_id = update.message.chat_id
    user_language_state[chat_id] = language  # Store the selected language

    # Display "Return" button to exit code input mode
    keyboard = [[KeyboardButton("↪️ Return")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"You selected {language}. Please enter your code. Press 'Return' when you're done.",
        reply_markup=reply_markup,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_code = update.message.text

    if user_code == "↪️ Return":
        # User exits code input mode
        user_language_state.pop(chat_id, None)
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
            "Exited code input mode. Select another language:",
            reply_markup=reply_markup,
        )
    elif chat_id in user_language_state:
        language = user_language_state[chat_id]
        # Execute the user's code in the selected language
        code_output = execute_code(content=user_code, language=language)
        await update.message.reply_text(code_output)
    else:
        await update.message.reply_text(
            "Please select a programming language to start running code."
        )


def error(update, context):
    logging.error(f"Update {update} caused error {context.error}")


async def handle_button_press(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    selected_language = update.message.text  # Text from button press
    if selected_language in LANGUAGES:
        language = LANGUAGES[selected_language]
        await run_code_command(update, context, language)
    else:
        await update.message.reply_text("Please select a valid programming language.")


if __name__ == "__main__":
    updater = ApplicationBuilder().token(API_KEY).build()

    # Commands
    updater.add_handler(CommandHandler("start", start_command))
    updater.add_handler(CommandHandler("help", help_command))
    updater.add_handler(CommandHandler("about", about_command))

    # Message handler for selecting a language or handling the "Return" button
    updater.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("|".join(LANGUAGES.keys())),
            handle_button_press,
        )
    )

    # Message handler for receiving and executing code
    updater.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Log errors
    updater.add_error_handler(error)

    # Run the bot
    updater.run_polling()
    updater.idle()
