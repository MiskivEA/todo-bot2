from dataclasses import dataclass
from environs import Env
from aiogram.fsm.storage.redis import Redis, RedisStorage


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    bot: TgBot
    storage: RedisStorage
    redis: Redis


def load_config(env_file_path=None):
    env = Env()
    env.read_env(env_file_path)

    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    config = Config(bot=TgBot(token=env('BOT_TOKEN')),
                    storage=storage,
                    redis=redis)
    return config
