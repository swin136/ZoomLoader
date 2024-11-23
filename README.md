# Zoom Video Loader
Программное обеспечение для скачивания сохраненной записи из Zoom по ссылке и паролю <!-- описание репозитория -->
## Установка (Windows)
У вас должны быть установлен Mozilla Firefox и Python 3

1. Клонирование репозитория 

```git clone https://github.com/swin136/ZoomLoader.git```

2. Переход в директорию Oxygen

```cd ZoomLoader```

3. Создание виртуального окружения

```python -m venv venv```

4. Активация виртуального окружения

```source venv/bin/activate```

5. Установка зависимостей

```pip3 install -r requirements.txt```

6. Скачайте последнюю версия geckodriver и поместите его в каталог core проекта

7. Скопируйте в корень проекта из каталога core файл input.txt

8. Запуск скрипта для демонстрации возможностей Oxygen

```python start_loader.py```
