# test_dimatech

### Запуск проекта через docker-compose
```bash
docker-compose up app
```

### Open API
https://localhost:8000/api/v1/docs

Для запуска ruff в режиме исправления
```bash
docker-compose run app bash
ruff format .
ruff check --fix .
```

### Миграции

Автогенерация миграций
```bash
docker-compose run app bash
alembic revision --autogenerate -m "Added ReportRequest table"
```

Запуск миграций
```bash
docker-compose run app bash
alembic upgrade head
```


### Данные для аутентификации
test_admin@example.com:adminpassword

test_user@example.com:userpassword

### Тестовый payload для payment webhook
```json
{
  "user_id": 2,
  "account_id": 1,
  "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
  "amount": 100,
  "signature": "d9ddc7614628c22213bf87eb5a445064832a132197336566f8f63bd7c35ab9b6"
}
```