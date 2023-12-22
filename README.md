С 1 по 7 задание выполненны в test.ipynb  
8 задание в 8. threads messages.py, 9 в 9. banking system.py, 11 в 11. sql_employees.py

10 задание выполенно в github_api.py. Для запуска нужно запустить следующие комманды
```bash
docker build -t github_api  .
docker run -it -d -p 5000:5000 github_api
```
У апи есть два эндпойнта, это POST `/add_user` с парраметром `username` и GET `all_users`
