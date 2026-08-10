# Django Backend

Backend для проекта InPar, построен на Django 4.2 с REST API.

## Структура проекта

```
backend/
├── config/          # Основная конфигурация Django
├── api/             # API приложение
├── static/          # Статические файлы
├── media/           # Загруженные файлы
├── manage.py        # Django управление
└── Dockerfile       # Docker конфигурация
```

## Быстрый старт

### Локальное развертывание

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Скопировать переменные окружения
cp .env.example .env

# Запустить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
```

### С Docker

```bash
# Запустить весь проект
docker-compose up -d

# Создать суперпользователя
docker-compose exec backend python manage.py createsuperuser

# Миграции
docker-compose exec backend python manage.py migrate
```

## API Endpoints

- `GET /api/health/` - Проверка статуса backend

## Администрирование

Администраторская панель доступна по адресу: `http://localhost:8000/admin/`

## Переменные окружения

Смотрите `.env.example` для полного списка переменных.
