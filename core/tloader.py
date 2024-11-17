import copy

import requests
import os
import math
import random
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

BUFFER_SIZE = 20_485_760
POOL_LENGTH = 8
OUT_FILE = 'all_parts'
DATA_DIR = 'data'
OUT_DIR = 'out'

def folders_init(data_dir: str, out_dir: str) -> bool:
    try:
        if not os.path.isdir(data_dir):
            os.makedirs(data_dir)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
    except PermissionError:
        print('Ошибка с правами доступа при создании каталога для записи файлов медиа.')
        return False
    except IOError:
        print('Ошибка с правами доступа при создании каталога для записи файлов медиа.')
        return False

    return True


def get_uniq_name() -> str:
    """
    Генерируем уникальное имя для файла с JSON-данными
    :return: str
    """
    random.seed()
    name = ""
    for i in range(10):
        probability = random.randint(0, 100)
        if probability > 30:
            name += chr(random.randint(65, 90))
        else:
            name += chr(random.randint(49, 57))
    # Вставить проверку уникальности имени
    return name


class LoaderMedia:
    """Наш класс для загрузки медиа"""

    def __init__(self, url:str, cookies:dict, headers:dict, data_dir=DATA_DIR,
                 out_dir=OUT_DIR, out_file=OUT_FILE, buffer_size=BUFFER_SIZE, pool_length=POOL_LENGTH):
        self.__url = url
        self.__cookies = cookies
        self.__headers = headers
        self.__data_dir = data_dir
        self.__out_dir = out_dir
        self.__out_file = out_file
        self.__buffer_size = buffer_size
        self.__media_total_size = self.get_size()
        self.__media_parts_cnt = math.ceil(self.__media_total_size / buffer_size)
        self.__task_list = []
        self.__pool_length = pool_length


        # инициализируем каталоги
        folders_init(data_dir=self.__data_dir, out_dir=self.__out_dir)

        # инициализируем список задач
        self.init_tasks()

    def __load_chunk(self, part_number: int):
        """Загружает часть медиа"""
        if (part_number > self.total_media_parts_count - 1) or (part_number < 0):
            raise ValueError
        # print(part_number)
        # Указываем адреса байтов для скачивания
        tmp_headers = copy.deepcopy(self.__headers)
        tmp_headers['range'] = (f'bytes={self.__task_list[part_number]['start_pos']}-'
                                f'{self.__task_list[part_number]['finish_pos']}')

        response = requests.get(
            url=self.__url,
            headers=tmp_headers,
            cookies=self.__cookies
        )

        if response.status_code == 206:
            # print(f'{self.__task_list[part_number]['start_pos']} ... '
            #       f'{self.__task_list[part_number]['finish_pos']} >>> ', end='')
            # print("\033[32m{}\033[0m".format('Ок'))
            self.__task_list[part_number]['is_downloaded'] = True
            # Записываем файл
            with open(os.path.join(self.__data_dir, self.__task_list[part_number]['rec_file_name']), 'wb') as rec_file:
                rec_file.write(response.content)
        else:
            # errors_count += 1
            # print("\033[31m{}\033[0m".format('Ошибка'))
            self.__task_list[part_number]['is_error'] = True

    def init_tasks(self):
        """Инициализируем параметры для скачивания медиа"""
        for i in range(self.__media_parts_cnt):
            start_position = self.__buffer_size * i
            finish_position = start_position + self.__buffer_size - 1
            if finish_position > (self.__media_total_size - 1):
                finish_position = self.__media_total_size - 1

            # print(f'{i} >>> {start_position }...{finish_position}')

            task = {
                'start_pos': start_position,
                'finish_pos': finish_position,
                'rec_file_name': f'{get_uniq_name()}.tmp',
                'is_error': False,
                'is_downloaded': False,
            }
            # print(task)
            self.__task_list.append(task)

    def load_all_pars(self):
        """Загрузка всех частей медиа"""
        # for i in range(self.total_media_parts_count):
        #     self.load_part(i)

        # for i in tqdm(range(self.total_media_parts_count), ncols=80, ascii=True, desc='Загрузка медиа'):
        #     self.load_part(i)

        # Новый вариант загрузки ...
        # Пытаемся запустить несколько загрузок

        task_total = self.__media_parts_cnt
        pool_list_cnt = self.__pool_length
        tasks = []
        # Формируем пул загрузок
        pools_cnt = math.ceil(task_total / pool_list_cnt)
        for i in range(pools_cnt):
            start = i * pool_list_cnt
            finish = start + pool_list_cnt - 1
            if finish > task_total - 1:
                finish = task_total - 1
            tasks.append([item for item in range(start, finish + 1)])
        # Сам запуск параллельного кода
        for task in tqdm(tasks, ncols=80, ascii=True, desc='Скачано пулов медиа', colour='GREEN'):
            with ThreadPoolExecutor(max_workers=len(task)) as pool:
                pool.map(self.__load_chunk, task)

        return


    @property
    def total_media_parts_count(self) -> int:
        """Возвращаем количество частей для скачивания видео"""
        return self.__media_parts_cnt

    @property
    def downloading_parts(self) -> int:
        """Возвращаем сколько частей медиа успешно скачано"""
        cnt = 0
        for item in self.__task_list:
            cnt += item['is_downloaded']

        return cnt

    def join_all_part(self) -> bool:
        """Объединяем все части видео"""
        out_data = b''
        for i in tqdm(range(self.total_media_parts_count), ncols=80, ascii=True,
                      desc='Объединение частей медиа', colour='RED'):
            try:
                with open(os.path.join(self.__data_dir, self.__task_list[i]['rec_file_name']), 'rb') as fp:
                    out_data += fp.read()
            except IOError:
                print(f'Во время объединения файлов обнаружены ошибки! >>> файл {self.__task_list[i]['rec_file_name']}')
                print('Работа сценария аварийно завершена!')
                return False
        # Записываем выходной файл
        try:
            with open(os.path.join(self.__out_dir, self.get_out_file_name), 'wb') as fp:
                fp.write(out_data)
        except IOError:
            print(f'Во время записи выходного файла произошла ошибка!')
            print('Работа сценария аварийно завершена!')
            return False

        return True

    @property
    def downloading_errors(self) -> int:
        """Возвращаем сколько частей медиа успешно скачано"""
        cnt = 0
        for item in self.__task_list:
            if item['is_error']:
                cnt += 1
        return cnt

    @property
    def get_out_file_name(self) -> str:
        """Возвращает имя выходного файла медиа из ссылки"""
        src_str = self.__url
        index = src_str.find('?')
        if index == -1:
            return self.__out_file
        s1 = src_str[:index][::-1]
        index = s1.find('/')
        if index == -1:
            return self.__out_file
        return s1[:index][::-1]

    @property
    def get_output_folder(self):
        """Возвращает имя каталога для выходного файла медиа """
        return self.__out_dir

    def __str__(self):
        """Возвращаем список заданий для скачивания"""
        return (
            f'Всего в списке задач для скачивания частей файла <<{self.get_out_file_name}>> - {len(self.__task_list)}\nСкачано частей - '
            f'{self.downloading_parts}')

    def get_size(self) -> int:
        """Получаем размер файла для последующего скачивания"""
        try:
            response = requests.head(
                url=self.__url,
                cookies=self.__cookies,
                headers=self.__headers,
            )
            size = int(response.headers.get('Content-Length'))
        except:
            size = None
        if (size is None) or (size == 110):
            size = -1
        # if size == 110:
        #     size = -1
        return size
    
    @property
    def media_size(self) -> int:
        return self.__media_total_size

    @staticmethod
    def format_size(size_in_bytes) -> str:
        """
        Форматированный вывод размера файла в Б/КБ/МБ/ГБ/ПБ
        :param size_in_bytes:
        :return: str
        """
        if size_in_bytes == 0:
            return  "0 Б"
        size_name = ("Б", "КБ", "МБ", "ГБ", "ПБ")
        i = int(math.floor(math.log(size_in_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_in_bytes / p, 2)
        return f"{s} {size_name[i]}"



