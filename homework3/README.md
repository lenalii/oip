**Deployment Manual**


Переход в папку со дз
```
cd /path/to/oip/homework3
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
pip install pymorphy2
```
Запуск создания инвертированного индекса
```
python inverted_index.py
```

Запуск булева поиска
```
python boolean_search.py
```