**Deployment Manual**

Переход в папку с первым дз
```
cd /path/to/oip/homework1
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
pip install requests beautifulsoup4
```
Запуск скрипта
```
python crawler.py
```