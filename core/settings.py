from environs import Env
from dataclasses import dataclass
import configparser


@dataclass
class ZoomVebParams:
    meet_url: str
    meet_pwd: str


@dataclass
class Settings:
    meeting_params: ZoomVebParams


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        meeting_params=ZoomVebParams(
            meet_url=env.str('zoom_meeting_url'),
            meet_pwd=env.str('zoom_meeting_pwd')
        )
    )


@dataclass
class AppSettings:
    buffer_size: int
    pool_length: int
    out_file_name: str
    tmp_data_dir: str
    out_data_dir: str
    driver_name: str
    delay_time: int


def read_app_settings(path: str):
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    return AppSettings(
        buffer_size=config.getint('Basic', 'buffer_size'),
        pool_length=config.getint('Basic', 'pool_length'),
        out_file_name=config.get('Basic', 'out_file_name'),
        tmp_data_dir=config.get('Basic', 'tmp_data_dir'),
        out_data_dir=config.get('Basic', 'out_data_dir'),
        driver_name=config.get('Basic', 'driver_name'),
        delay_time=config.getint('Basic', 'delay_time'),

    )


app_settings = read_app_settings('config.ini')
zoom_settings = get_settings('input.txt')
