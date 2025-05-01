**Deployment Manual**

Вначале выполнить код из предыдущих дз

Переход в папку с демо
```
cd /path/to/oip/demo
```
Создание виртуального окружения
```
python3 -m venv venv
```
Активация виртуального окружения:

Для Windows:
```
venv\Scripts\activate
```
Для macOS/Linux:
```
source venv/bin/activate
```
Установка зависимостей
```
pip install -r demo/requirements.txt
```
Запуск скрипта
```
python app.py
```