## **Локальный запуск проекта**
```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python3 manage.py migrate
Launch a project:
python3 manage.py runserver
```

## **Эндпоинты**
**Регистрация**
```
POST api/users/
```
Request body:
```
{
    "username": "user",
    "password": "password"
}
```
**Вход:**
```
POST auth/token/login/
```
Request body:
```
{
    "username": "user",
    "password": "password"
}
```
В ответ придет токен, который нужно передавать в заголовке запросов, связанных с избранными

**Новости:**
```
GET api/news/
```
**Все доступные криптовалюты:**
```
GET api/currencies/
```
Можно искать по символьному коду и выбирать валюту для отображения курса (по умолчанию USD):
```
GET api/currencies?symbol=BTC&convert=EUR
```
**Вывод одной валюты по символьному коду:**
```
GET api/currencies/{код}/
```
**Добавление и удаление валюты в избранное:**
```
POST api/currencies/{код}/favorite/
DELETE api/currencies/{код}/favorite/
```
**Вывод избранных валют:**
```
GET api/currencies/favorites/
```
Тут так же можно выбрать валюту для курса:
```
GET api/currencies/favorites?convert=EUR
```
