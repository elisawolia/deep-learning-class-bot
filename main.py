import threading
import uvicorn

from bot.core_bot import bot
from backend.service import app

def start_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8086)

def start_telegram_bot():
    bot.start()

if __name__ == "__main__":
    t1 = threading.Thread(target=start_fastapi)
    t2 = threading.Thread(target=start_telegram_bot)

    t1.start()
    t2.start()

    t1.join()
    t2.join()