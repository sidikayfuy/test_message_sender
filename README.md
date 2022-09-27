# Test work message sender

Для запуска необходимо загрузить архив с кодом и извлечь. 

Через терминал перейти в папку с извлеченными файлами и запустить команду:

````
docker-compose up --build -d && docker exec -it test_message_sender-main-webapp-1 bash -c "celery -A test_message worker --loglevel=info" 
````

