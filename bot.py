from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import os

# --- Bot Token and Username ---
# Define your Telegram bot token and bot username here.
# IMPORTANT: Replace 'your_token_here' and '@your_bot_username' with your actual bot token and username.
TOKEN: Final[str] = 'your_token_here'
BOT_USERNAME: Final[str] = '@your_bot_username'

# --- Setup logging ---
# This helps to log info and errors in the console for debugging.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Command Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for the /start command.
    When user sends /start, bot replies with a welcome message.
    """
    await update.message.reply_text("✅ Bot started successfully!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for the /help command.
    When user sends /help, bot replies with instructions.
    """
    await update.message.reply_text("ℹ️ Send me a message and I'll try to respond!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for a custom command (/custom).
    You can define your own commands like this.
    """
    await update.message.reply_text("🛠️ This is a custom command.")

# --- Message Response Logic ---

def handle_response(text: str) -> str:
    """
    This function processes the user's text message and returns a response.
    It converts text to lowercase and matches some predefined keywords.
    """
    processed = text.lower()

    if "input 1" in processed:
        return "✅ You triggered input 1 response!"
    elif "input 2" in processed:
        return "✅ You triggered input 2 response!"
    else:
        return "🤖 Sorry, I didn't understand that."

# --- Message Handler ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function handles incoming text messages from users or groups.
    It distinguishes between private chats and group chats.
    For group chats, the bot only responds if it's mentioned by its username.
    """
    message_type = update.message.chat.type
    text = update.message.text

    # Log the incoming message info
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Check if the message is from a group or supergroup
    if message_type in ['group', 'supergroup']:
        # If the bot's username is mentioned in the message
        if BOT_USERNAME in text:
            # Remove the bot username from the message text
            text = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(text)
        else:
            # If bot is not mentioned, do not respond
            return
    else:
        # For private chats, respond to any text message
        response = handle_response(text)

    # Log the bot's response
    print('Bot:', response)

    # Send the response message back to the user/group
    await update.message.reply_text(response)

# --- Error Handler ---

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """
    This function logs any errors that occur during updates.
    """
    logging.error(f'Update {update} caused error {context.error}')

# --- Main function to start the bot ---

if __name__ == '__main__':
    print('Starting bot...')

    # Create the Application and pass the bot's token
    app = Application.builder().token(TOKEN).build()

    # Add command handlers to the bot
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Add message handler for text messages excluding commands
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add error handler
    app.add_error_handler(error_handler)

    print('Polling...')
    # Start polling updates from Telegram
    app.run_polling(poll_interval=3)
