from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import time
import os
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = open('config/token.conf', 'r').read().replace("\n", "")
message_list = os.listdir("message")

if not os.path.exists("logs"):
    os.makedirs("logs")

def welcome(bot, update):
    if(update.message.new_chat_member):
        open("logs/logs_" + time.strftime('%d_%m_%Y') + ".txt","w").write("\nupdate status: " + str(update))
    	chat_id = update.message.chat.id
        new_user = ""
        message_rnd = random.choice(message_list)
        WELCOME_MESSAGE = open('message/' + message_rnd , 'r').read().replace("\n", "")

        if(update.message.new_chat_member.username != ""):
            new_user = "@" + update.message.new_chat_member.username;
        else:
            new_user = update.message.new_chat_member.first_name;

    	bot.sendMessage(chat_id=chat_id, text=WELCOME_MESSAGE.replace("{{username}}",str(new_user)), parse_mode='Markdown')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
    open("logs/error.txt","w").write("\nupdate status: " + str(update) + "\nerror: " + str(error))

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update, welcome))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
