from environs import Env
from dataclasses import dataclass


@dataclass
class Zoom_Veb_Params:
    meet_url: str
    meet_pwd: str


@dataclass
class Settings:
    meeting_params: Zoom_Veb_Params


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        meeting_params=Zoom_Veb_Params(
            meet_url=env.str('zoom_meeting_url'),
            meet_pwd=env.str('zoom_meeting_pwd')
            )
    )


zoom_settings = get_settings('input.txt')

