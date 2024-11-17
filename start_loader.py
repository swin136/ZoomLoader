from core.loader_headers import LoaderLinkParams
from core.settings import settings
from core.tloader import LoaderMedia

import datetime


def main() -> None:
    """Реализация основной бизнес-логики"""
    start_processing = datetime.datetime.now()
    print(f'Начало операции >>> {start_processing.strftime("%d-%m-%Y %H:%M:%S")}')
    ...
    loader_headers = LoaderLinkParams(zoom_url=settings.meeting_params.meet_url, zoom_passwd=settings.meeting_params.meet_pwd)
    if loader_headers.load_params() == 0:
        print(loader_headers)
        # print(loader_headers.get_headers)
        # print(loader_headers.get_cookies)
        # Код загрузки
        my_media = LoaderMedia(url=loader_headers.media_url, cookies=loader_headers.get_cookies, headers=loader_headers.get_headers)
        # Определяем размер файла для скачивания
        f_media_size = my_media.media_size
        # Ошибка при получении размеров скачиваемого файла
        if f_media_size == -1:
            print("\033[31m{}"
                "\033[0m".format('Ошибка при доступе к параметрам файла медиа - аварийное завершение программы!'))
            return

        print(f'Размера файла медиа для скачивания >>> ', end='')
        print("\033[32m{}\033[0m".format(f'{LoaderMedia.format_size(f_media_size)}'))
        # my_media = LoaderMedia(f_media_size, url=loader_headers.media_url, cookies=loader_headers.get_cookies, headers=loader_headers.get_headers)
        # print(my_media)
        my_media.load_all_pars()
        if my_media.downloading_errors > 0:
            print("\033[31m{}\033[0m".format('Во время скачивания контента обнаружены ошибки!'))
            print('Работа сценария аварийно завершена!')
            return
        # Объединяем части видео
        if not my_media.join_all_part():
            print("\033[31m{}\033[0m".format('Во время объединения частей скаченного контента обнаружены ошибки!'))
            print('Работа сценария аварийно завершена!')
            return

        print(f'Успешно скачан файл ', end='')
        print("\033[34m{}\033[0m".format(f'{my_media.get_out_file_name}'))
        print(f'Файл находится в каталоге ', end='')
        print("\033[32m{}\033[0m".format(f'{my_media.get_output_folder}'))
        
    ...
    finish_processing = datetime.datetime.now()
    print(f'Завершение работы программы  >>> {finish_processing.strftime("%d-%m-%Y %H:%M:%S")}')
    delta_processing = finish_processing - start_processing
    print("Затрачено времени на работу скрипта : ", end='')
    print("\033[32m{}\033[0m".format(f'{round(delta_processing.total_seconds(), 3)} сек.\n'))

    print('До свидания!')
    return


if __name__ == "__main__":
    main()
