import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackContext,
    filters,
)
from code_runner import execute_code
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.info("Starting bot...")

expecting_code_input = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("/runcode")],  # Regular button for running code
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Hello goobler. I'm Meower, your bot assistant!", reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello goobler. Use /runcode to run Python code.")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello goobler. This is a custom command.")


async def run_code_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    expecting_code_input[chat_id] = True
    await update.message.reply_text("Please enter your Python code:")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text

    if expecting_code_input.get(chat_id):
        code_output = execute_code(text)
        await update.message.reply_text(code_output)
        expecting_code_input[chat_id] = False
    else:
        await update.message.reply_text(
            "I received your message but wasn't expecting code."
        )


def error(update, context):
    logging.error(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    updater = ApplicationBuilder().token(API_KEY).build()

    # Commands
    updater.add_handler(CommandHandler("start", start_command))
    updater.add_handler(CommandHandler("help", help_command))
    updater.add_handler(CommandHandler("custom", custom_command))
    updater.add_handler(CommandHandler("runcode", run_code_command))

    # Messages
    updater.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Log errors
    updater.add_error_handler(error)

    # Run the bot
    updater.run_polling()
    updater.idle()
