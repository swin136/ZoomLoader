from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

from core.settings import zoom_settings

import time

import os

TIMER_FOR_WAIT = 20
FIREFOX_DRIVER_NAME = 'geckodriver.exe'

# selenium.common.exceptions.NoSuchDriverException

class LoaderLinkParams:
    """
    Класс для загрузки параметров видео с Zoom под паролем
    """

    def __init__(self, zoom_url: str, zoom_passwd: str, timer_period=TIMER_FOR_WAIT, driver_name = FIREFOX_DRIVER_NAME):
        self.__url = zoom_url.strip()
        self.__passwd = zoom_passwd.strip()
        self.__timer_for_wait = timer_period
        self.__driver_name = driver_name
        # инициализируем Получаемые параметры
        self.__media_url = None
        self.__get_headers = None
        self.__get_cookies = None

    def load_params(self):
        driver = None
        try:
            options = Options()
            options.add_argument('--headless')
            service = Service(executable_path=os.path.join(os.getcwd(), 'core', self.__driver_name))
            driver = webdriver.Firefox(service=service, options=options)
            driver.get(self.__url)
            driver.implicitly_wait(self.__timer_for_wait * 3)
            # Ищем поле для ввода кода доступа к конференции
            element = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
            element.send_keys(self.__passwd)
            time.sleep(self.__timer_for_wait)
            # Ищем кнопку и жмем на нее
            button = driver.find_element(By.CSS_SELECTOR,
                                         'button[class="zm-button--primary zm-button--large zm-button"]')
            button.send_keys(Keys.RETURN)
            print('Проверка кода доступа ... ',end='')
            time.sleep(self.__timer_for_wait)
            try:
                driver.find_element(By.CLASS_NAME, 'zm-alert__content')
                # print('Код доступа неверен!')
                print("\033[31m{}\033[0m".format('Ошибка'))
                return -1
            except exceptions.NoSuchElementException:
                # print('Код для Zoom-ссылки верный!')
                print("\033[32m{}\033[0m".format('ОК'))

            is_continue = True
            print('Ищем ссылку на видео в Zoom ', end='')
            while is_continue:
                print('.', end='')
                time.sleep(self.__timer_for_wait)
                for request in driver.requests:
                    if request.response:
                        if request.response.status_code == 206 and request.response.headers[
                            'Content-Type'] == 'video/mp4':
                            is_continue = False
                            print("\033[32m{}\033[0m".format(' ОК\n'))
                            self.__media_url = request.url
                            # print(r
                            # print(dir(request.headers))
                            # print('*'*20)
                            # print(type(request.headers))
                            # print('*'*20)
                            cookie = ''
                            # print('user_headers = {\n')
                            self.__get_headers = {}
                            self.__get_cookies = {}
                            for item in request.headers:
                                if item == 'Cookie':
                                    cookie = request.headers[item]
                                    continue
                                # print(f"'{item}' : '{request.headers[item]}',")
                                self.__get_headers[item] = request.headers[item]
                                # log_to_save = log_to_save + f"\t'{item}': '{request.headers[item]}',\n"
                            # print('}')
                            # log_to_save = log_to_save + '}\n'
                            # print('*' * 20)
                            cookie_list = cookie.split(';')
                            # print('COOKIES = {')
                            # log_to_save = log_to_save + '\nCOOKIES = {\n'
                            for item in cookie_list:
                                item_separate = item.split('=')
                                self.__get_cookies[item_separate[0].strip()] = item_separate[1]
                            return 0
                                # print(f"'{item_separate[0].strip()}' : '{item_separate[1]}',")
                                # log_to_save = log_to_save + f"\t'{item_separate[0].strip()}': '{item_separate[1]}',\n"
                            # print('}')
                            # log_to_save = log_to_save + '}\n'
                            # print(cookie_list)
                            # print('*' * 20)
                            # with open(LOG_FILE, "w", encoding="utf-8") as log_file:
                            #     log_file.write(log_to_save)

        except exceptions.NoSuchDriverException:
            print('Ошибка драйвера Firefox!')
            return -1
        except exceptions.NoSuchElementException:
            print('Неверная ссылка!')
            return -1

        finally:
            if driver is not None:
                driver.close()

    def __str__(self):
        return f'Ссылка на видео в Zoom: {self.media_url}\n'

    @property
    def get_headers(self):
        return self.__get_headers


    @property
    def get_cookies(self):
        return self.__get_cookies
    
    @property
    def media_url(self):
        return self.__media_url


if __name__ == "__main__":
    # ZOOM_URL = 'https://us06web.zoom.us/rec/share/oMwXJ3EU9N2tERUwhlsMGWspte8zV2UM5ZhCfkexiC9uZMtIJBJZabEoioBA_a6Q.v1NLFiDaRn1L6nNV'
    # INPUT_CODE = '1EGKQ+3m'
    # loader_headers = LoaderLinkParams(zoom_url=ZOOM_URL, zoom_passwd=INPUT_CODE)
    loader_headers = LoaderLinkParams(zoom_url=zoom_settings.meeting_params.meet_url, zoom_passwd=zoom_settings.meeting_params.meet_pwd)
    if loader_headers.load_params() == 0:
        print(loader_headers)
        print(loader_headers.get_headers)
        print(loader_headers.get_cookies)
