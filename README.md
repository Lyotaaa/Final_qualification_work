### Технического задание на данный проект (без продвинутой части)

Файл находиться в папке Netology, или перейдите по активной ссылке [README.md](/Netology/README.md)

## Установка и запуск проекта

### Для запуска необходимо заполнить файл [.env.template](./My_project/my_project/.env.template)
##### Отмеченные пункты галочкой и цветом требуют изменений

- [x] <font color="black and red">SECRET_KEY</font> = Вставьте ваш секретный ключ
- [x] <font color="black and red">DEBUG</font> = Выберите True или False
- [ ] ALLOWED_HOSTS=localhost
- [ ] DB_ENGINE=django.db.backends.postgresql
- [x] <font color="black and red">POSTGRES_DB</font> = Вставьте название вашей БД
- [ ] POSTGRES_USER = postgres
- [x] <font color="black and red">POSTGRES_PASSWORD</font> ="Password for your database"
- [ ] DB_HOST=127.0.0.1
- [x] <font color="black and red">DB_PORT</font> = Укажите удобный порт (не забудьте прописать такой же порт в файле [docker-compose.yaml](/My_project/docker-compose.yml), <font color="green">По умолчанию 5434</font>)

##### После редактирвоания файла удалите расширение из **.env.<font color="red">template</font>** в **.env**