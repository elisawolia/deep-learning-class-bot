import telebot
import os
from database.model import subscribe, unsubscribe
from database.model import SessionLocal

class Bot:
    
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        
        @self.bot.message_handler(commands=['start'])
        def start_handler(message):
            db = SessionLocal()
            try:
                subscribe(message.chat.id, db)
                self.bot.reply_to(message, 'Добрый день! Теперь вы сможете получать уведомления от бота. Чтобы отписаться используйте команду /stop.')
            except Exception:
                self.bot.reply_to(message, 'Вы уже подписаны на бота. Чтобы отписаться используйте команду /stop.')
            finally:
                db.close()
            

        
        @self.bot.message_handler(commands=['stop'])
        def stop_handler(message):
            db = SessionLocal()
            try:
                unsubscribe(message.chat.id, db)
                self.bot.reply_to(message, 'Вы больше не будете получать уведомления от бота. Чтобы подписаться используйте команду /start.')
            except Exception:
                self.bot.reply_to(message, 'Вы уже отписаны от бота. Чтобы подписаться используйте команду /start.')
            finally:
                db.close()

        
        @self.bot.message_handler(commands=['ping'])
        def ping_handler(message):
            self.bot.reply_to(message, 'Pong')

    def start(self):
        self.bot.infinity_polling(none_stop=True)

# Telegram Bot Configuration
TOKEN = os.environ.get('BOT_TOKEN', '')
bot = Bot(token=TOKEN)