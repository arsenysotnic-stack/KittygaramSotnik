# Kittygram — Паспорт здоровья кота (Трек 13)

REST API для управления котиками и ведения паспортов здоровья питомцев.

## Стек

- Python 3.11, Django 4.2, Django REST Framework 3.14
- SQLite (по умолчанию)
- Swagger UI через drf-yasg

---

## Локальный запуск

```bash
# 1. Создать и активировать виртуальное окружение
python -m venv .venv
# Linux / macOS:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (cmd):
.venv\Scripts\activate.bat

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Создать .env из примера
cp .env.example .env           # Linux / macOS
# copy .env.example .env       # Windows

# 4. Применить миграции
python manage.py migrate

# 5. Создать суперпользователя (опционально)
python manage.py createsuperuser

# 6. Запустить сервер
python manage.py runserver
```

---

## Запуск через Docker

```bash
# Собрать и запустить
docker compose up -d --build
```

Сервер будет доступен на `http://localhost:8000/`.

---

## Переменные окружения (.env)

| Переменная | Описание | Пример |
|---|---|---|
| `SECRET_KEY` | Секретный ключ Django | `django-insecure-...` |
| `DEBUG` | Режим отладки | `True` / `False` |
| `ALLOWED_HOSTS` | Разрешённые хосты (через запятую) | `localhost,127.0.0.1` |

---

## API

| URL | Описание |
|---|---|
| `http://127.0.0.1:8000/api/swagger/` | Swagger UI — вся документация |
| `http://127.0.0.1:8000/api/redoc/` | ReDoc |
| `http://127.0.0.1:8000/admin/` | Админка Django |

### Аутентификация

```bash
# Получить токен
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

Использовать токен в заголовке: `Authorization: Token <ваш_токен>`

---

### Эндпоинты котиков

```bash
# Список котиков
curl http://127.0.0.1:8000/api/cats/

# Создать котика
curl -X POST http://127.0.0.1:8000/api/cats/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Барсик", "color": "рыжий", "birth_year": 2020}'

# Мои котики
curl http://127.0.0.1:8000/api/cats/my_cats/ \
  -H "Authorization: Token <token>"
```

---

### Паспорт здоровья

```bash
# Создать запись здоровья
curl -X POST http://127.0.0.1:8000/api/health/records/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "cat": 1,
    "record_type": "visit",
    "title": "Плановый осмотр",
    "date": "2024-03-15",
    "next_date": "2025-03-15",
    "doctor_name": "Иванова А.В."
  }'

# Отметить запись выполненной
curl -X POST http://127.0.0.1:8000/api/health/records/1/complete/ \
  -H "Authorization: Token <token>"

# Предстоящие процедуры кота (id=1)
curl http://127.0.0.1:8000/api/health/records/cat/1/upcoming/

# Все записи кота (id=1)
curl http://127.0.0.1:8000/api/health/records/cat/1/

# Фильтрация записей
curl "http://127.0.0.1:8000/api/health/records/?record_type=visit&date_from=2024-01-01&date_to=2024-12-31"

# Список клиник
curl http://127.0.0.1:8000/api/health/clinics/

# Добавить клинику
curl -X POST http://127.0.0.1:8000/api/health/clinics/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Добрый Ветеринар", "address": "ул. Пушкина, 1", "phone": "+7-999-123-45-67"}'
```

---

### Типы записей здоровья

| Код | Название |
|---|---|
| `visit` | Визит к врачу |
| `procedure` | Процедура |
| `medication` | Лекарство |
| `vaccination` | Вакцинация |
| `analysis` | Анализы |
