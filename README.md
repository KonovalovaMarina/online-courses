# online-courses-2

###### Билд
```shell
docker-compose build web
```

###### Создание демо базы

```shell
docker-compose up -d db
docker-compose run --rm web python -m app demo
```

###### Запуск
```shell
mkdir -p app/uploads # создаем директорию для медиа файлов
docker-compose up -d ngrok
docker-compose up web
```
