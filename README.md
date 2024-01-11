### Технического задание на данный проект (без продвинутой части)

Файл находиться в папке Netology, или перейдите по активной ссылке [README.md](/Netology/README.md)

## Установка и запуск проекта

### Для запуска необходимо заполнить файл [.env.template](./My_project/my_project/.env.template)
#### Отмеченные пункты галочкой требуют изменений

- [x] <font color="black and red">SECRET_KEY</font> = Вставьте ваш секретный ключ
- [x] <font color="black and red">DEBUG</font> = Выберите True или False
- [ ] ALLOWED_HOSTS=localhost
- [ ] DB_ENGINE=django.db.backends.postgresql
- [x] <font color="black and red">POSTGRES_DB</font> = Вставьте название вашей БД
- [ ] POSTGRES_USER = postgres
- [x] <font color="black and red">POSTGRES_PASSWORD</font> ="Password for your database"
- [ ] DB_HOST=127.0.0.1
- [x] <font color="black and red">DB_PORT</font> = Укажите удобный порт (не забудьте прописать такой же порт в файле [docker-compose.yaml](/My_project/docker-compose.yml), <font color="green">По умолчанию 5434</font>)

#### После редактирвоания файла удалите расширение из **.env.<font color="red">template</font>** в **.env**

### Перейдите через терминал в папку с проектом
```
cd My_project
```
### Создайте вертуально окружение
```
python -m venv "Название вашего окружения (по умолчанию venv)"
```
### Активируйте вертуальное окружение
```
"Название вашего окружения (по умолчанию venv)"/Scripts/Activate
```
### Установите зависимости
```
pip install -r requirements.txt
```
### Запустить файл docker-compose.yaml командой. Для создания БД.
```
docker compose up -d
```
### Сформируйте базу данных, с которой будет работать приложение следующей командой
```
python manage.py makemigrations
```
### Примените миграции к вашей базе данных следующей командой
```
python manage.py migrate
```
### Запустите приложение следующей командой
```
python manage.py runserver
```
### Запустите тесты следующей командой
```
pytest
```
### Вы можете выполнить различные запросы через файл [requests-examples.http](/My_project/requests-examples.http)
### Для входа как администратор, необходимо создать суперпользователя
```
python manage.py createsuperuser
```
### Перейдите по ссылке и заполните созданные логин и пароль

http://127.0.0.1:8000/admin

#### Работу с базой данных можно провести через админку. Для быстрого заполнения БД используйте следующий метод в файле [requests-examples.http](/My_project/requests-examples.http)
```python
POST {{baseUrl}}/partner/update
Content-Type: application/json
Authorization: Token dcb47f10d5c351488736bc230d1aaed10d8009c1

{
  "url": 
  "https://raw.githubusercontent.com/Lyotaaa/Final_qualification_work/main/My_project/data/shop1.yaml"
}
```
#### Также все данные можно заполнить через администратора
### Посмотреть данные можно посмотреть через администратора или напрямаю через подключение к базе данных. Параметры для подключения такие же как вы указали в файле [.env.template](env.template). Обратите внимение на PORT: 5434.
```
* POSTGRES_USER = postgres
* POSTGRES_PASSWORD = Ваш пароль
* POSTGRES_DB = Название базы данных
* DB_HOST = 127.0.0.1
* DB_PORT = 5434
```


