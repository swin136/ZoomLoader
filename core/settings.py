from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    meet_url: str
    meet_pwd: str


@dataclass
class Settings:
    meeting_params: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        meeting_params=Bots(
            meet_url=env.str('zoom_meeting_url'),
            meet_pwd=env.str('zoom_meeting_pwd')
            )
    )


settings = get_settings('input.txt')

