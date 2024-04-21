import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import user_commands, creditor
logging.basicConfig(level=logging.INFO)
async def main():
    #Вставить сюда токен скоего бота
    bot = Bot(token=YOUR_BOT_TOKEN)
    dp = Dispatcher()


    dp.include_routers( user_commands.router,creditor.router,)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())