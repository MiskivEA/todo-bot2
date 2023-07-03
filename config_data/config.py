from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    bot: TgBot


def load_config(env_file_path=None):
    env = Env()
    env.read_env(env_file_path)
    config = Config(bot=TgBot(token=env('BOT_TOKEN')))
    return config
