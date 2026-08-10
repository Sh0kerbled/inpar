# Динамическое ценообразование на основе курса доллара

Реализована полная система ценообразования, где:

- ✅ Цены в админ-панели вводятся в **USD**
- ✅ На фронтенде цены динамически конвертируются в **KZT**
- ✅ В админ-панели показывается **preview цены в тенге**
- ✅ Курс доллара легко меняется через переменную окружения

## 🎯 Ключевые возможности

### 1. Админ-панель

- Ввод цены в долларах США
- Автоматический preview конвертированной цены в KZT
- Отображение текущего курса при загрузке

### 2. Публичная часть

- Все цены отображаются в KZT
- Динамическое обновление при изменении курса
- Поддержка fallback расчета на фронтенде

### 3. API

- Новый endpoint `/api/exchange-rate/` для получения курса
- Все продукты возвращают `price_usd` и `price_kzt`

## 📝 Чек-лист внедрения

- [x] Backend: Model - переименовано price → price_usd
- [x] Backend: Settings - добавлена переменная USD_TO_KZT_RATE
- [x] Backend: Serializers - добавлены price_kzt calculated fields
- [x] Backend: Views - новый endpoint для курса
- [x] Backend: Migration - миграция БД
- [x] Frontend: AdminProductForm - форма ввода price_usd с preview
- [x] Frontend: ProductsPage - отображение цен в KZT
- [x] Frontend: ProductDetailPage - отображение цен в KZT

## 🚀 Развертывание

```bash
# 1. Применить миграцию БД
python manage.py migrate

# 2. Перезагрузить приложение
# или использовать скрипт
bash backend/migrate_prices.sh

# 3. Установить/изменить курс (опционально)
export USD_TO_KZT_RATE=480
```

## 💱 Изменение курса

### Вариант 1: Переменная окружения

```bash
USD_TO_KZT_RATE=475
```

### Вариант 2: Docker Compose

```yaml
services:
  backend:
    environment:
      - USD_TO_KZT_RATE=475
```

### Вариант 3: .env файл

```
USD_TO_KZT_RATE=475
```

## 📊 Примеры использования

### Добавление товара

1. Админ-панель → "Добавить товар"
2. Ввести название, описание
3. **Цена в USD**: 500
4. Preview показывает: **≈ 230,000 ₸** (с курсом 460)
5. Сохранить

### На публичной странице

- Каталог: отображает цену в KZT
- Детали товара: отображает цену в KZT
- При изменении курса - автоматически обновляется

## 🔧 API примеры

### Получить курс

```bash
GET /api/exchange-rate/
```

Response:

```json
{
  "rate": 460.0,
  "currency_from": "USD",
  "currency_to": "KZT"
}
```

### Получить товары

```bash
GET /api/products/
```

Response:

```json
{
  "results": [
    {
      "id": 1,
      "name": "Товар",
      "price_usd": 500.00,
      "price_kzt": 230000.00,
      ...
    }
  ]
}
```

## 📝 Заметки

- Курс по умолчанию: 460 KZT за 1 USD
- Цена вычисляется в serializers, поэтому всегда актуальна
- На фронтенде есть fallback расчет на случай отсутствия price_kzt
- Миграция полностью обратима

## 📚 Файлы с документацией

- [PRICE_MIGRATION.md](./PRICE_MIGRATION.md) - полная документация миграции
- [backend/migrate_prices.sh](./backend/migrate_prices.sh) - скрипт применения миграции
- [backend/convert_prices.py](./backend/convert_prices.py) - скрипт для проверки данных
