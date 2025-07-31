from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: final = '8467743108:AAFjJxy6vFx8FIfTjuY7rroF3u-ge2wHs_Q'
Bot_username: final = '@Check2789_bot'

async def start_command(update: Update , context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! Im check')

async def help_command(update: Update , context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Im check , How can I help you')

def handle_response(text: str) -> str:
    processed: str = text.lower()
    if "Hello" in processed:
        return 'Hey there!'
    
    if "How are you" in processed:
        return 'Im good'
    
    return 'I do not understand you wrote....'

async def handle_messege(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type

    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if Bot_username in text:
            new_text: str = text.replace(Bot_username, '').strip()

            response: str = handle_response(new_text)

        else:
            return
    else:
        response: str = handle_response(text)  

    print('Bot:', response)

    await update.message.reply_text(response)



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':

    print('starting bot...')

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))



    app.add_handler(MessageHandler(filters.TEXT, handle_messege))

    app.add_error_handler(error)


    print('polling...')
    app.run_polling(poll_interval=3)