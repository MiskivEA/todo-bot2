import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from handlers.user_handlers import router
from config_data.config import load_config


async def main():
    config = load_config()
    bot = Bot(token=config.bot.token,
              parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(router)

    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/support',
                   description='Поддержка'),
        BotCommand(command='/contacts',
                   description='Другие способы связи'),
        ]

    await bot.set_my_commands(main_menu_commands)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
