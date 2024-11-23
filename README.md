# Zoom Video Loader
Программное обеспечение для скачивания сохраненной записи из Zoom по ссылке и паролю <!-- описание репозитория -->
## Установка (Windows)
У вас должны быть установлены Mozilla Firefox и Python 3

1. Клонирование репозитория 

```git clone https://github.com/swin136/ZoomLoader.git```

2. Переход в директорию ZoomLoader

```cd ZoomLoader```

3. Создание виртуального окружения

```python -m venv .venv```

4. Активация виртуального окружения

```.venv\Scripts\activate```

5. Установка зависимостей

```pip install -r requirements.txt```

6. Скачайте последнюю версия geckodriver.exe нужной (32 или 64) версии с https://github.com/mozilla/geckodriver/releases, распакуйте и поместите его в каталог <b>core</b> проекта

7. Скопируйте в корень проекта из каталога <b>core</b> файл <b>input.txt.example</b>, переименуйте его в <b>input.txt</b> и поместите туда актуальные данные (логин/пароль) для доступа к видео Zoom

8. Запуск скрипта для демонстрации возможностей ZoomLoader

```python start_loader.py```

## Поддержка
Если у вас возникли сложности или вопросы по использованию пакета напишите на электронную почту <i@kamenev-7.ru>.
