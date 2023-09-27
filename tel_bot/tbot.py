import os
import hashlib
import subprocess
from telegram import Update
from utils.logging import zlogger
from telegram.ext import (Updater,
    CommandHandler, MessageHandler,
    Filters, ConversationHandler,
    CallbackContext)

TBOT_TAPI = os.environ['tbot_tapi']
TBOT_CRED = os.environ['tbot_cred']

# these are for saving interactive input state
USERNAME, PASSWORD = range(2)


# Command handlers

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Hello! I'm nano1-team-bot. Type /help to see available commands."
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Available commands:\n"
                              "/start - Start the bot\n"
                              "/help - Show this help message\n"
                              "/updatesite - Update the site (requires username and password)")


def update_site_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Please enter your username:")
    return USERNAME


def receive_username(update: Update, context: CallbackContext) -> int:
    context.user_data['username'] = update.message.text
    update.message.reply_text("Please enter your password:")
    return PASSWORD


def receive_password(update: Update, context: CallbackContext) -> int:
    username = context.user_data['username']
    password = update.message.text
    
    print(f"checking username and password {username}:{password}")
    try:
        input_cred = hashlib.sha256(
            (username+":"+password).encode()
        ).hexdigest()
        print(input_cred, TBOT_CRED)

        if input_cred==TBOT_CRED:
            # be sure that its executable
            print(f"start update process")
            update.message.reply_text("starting udpate process, please waite...")
            output = subprocess.run(
                ["/home/zerobits01/market-automation-tools/tel_bot/utils/update.sh"], 
                shell=True
            )
            print(output)
            update.message.reply_text(f"output result: {output}")
            if output.returncode == 0:
                update.message.reply_text(f"Site updated for username: {username}")
            else:
                update.message.reply_text(f"Site couldnt be updated please contact @zerobits01")
            print("done")
        else:
            update.message.reply_text(f"username or password is wrong")
            
        return ConversationHandler.END
    except Exception as e:
        print(e)


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Update process cancelled.")
    return ConversationHandler.END


def main():
    # Set your bot token here
    token = TBOT_TAPI
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    
    # how to define interactive inputs to get the input from user
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('updatesite', update_site_start)],
        states={
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, receive_username)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, receive_password)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
