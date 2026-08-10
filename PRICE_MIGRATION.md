# Миграция на динамическое ценообразование в USD

## Описание изменений

Реализована система ценообразования на основе доллара США (USD) с динамической конвертацией в казахстанские тенге (KZT). Все цены в админ-панели теперь вводятся в USD, а для клиентов отображаются в KZT в зависимости от текущего курса обмена.

## Изменения Backend

### 1. Model (api/models.py)

- Переименовано поле `price` → `price_usd` в модели Product
- Добавлена справка о том, что это цена в USD

### 2. Settings (config/settings.py)

- Добавлена переменная `USD_TO_KZT_RATE = 460.0` для хранения курса доллара
- Может быть переопределена через переменную окружения `USD_TO_KZT_RATE`

### 3. Serializers (api/serializers.py)

- **ProductListSerializer**: добавлен field `price_kzt` (calculated field)
- **ProductDetailSerializer**: добавлен field `price_kzt` (calculated field)
- **ProductCreateUpdateSerializer**: обновлено на использование `price_usd`
- **OrderSerializer**: добавлен field `product_price_kzt` для отображения цены товара в KZT

### 4. Views (api/views.py)

- Добавлен новый endpoint `GET /api/exchange-rate/` для получения текущего курса
- Возвращает JSON: `{ rate: 460.0, currency_from: "USD", currency_to: "KZT" }`

### 5. URLs (api/urls.py)

- Добавлен маршрут для endpoint `/api/exchange-rate/`

### 6. Migration (api/migrations/0002_alter_product_price.py)

- Переименовано поле `price` на `price_usd`
- Обновлены индексы

## Изменения Frontend

### 1. AdminProductForm.vue

- Изменена форма для ввода `price_usd` вместо `price`
- Добавлен динамический preview конвертированной цены в тенге
- При изменении цены в USD автоматически показывает эквивалент в KZT
- При загрузке страницы получает текущий курс через API

### 2. ProductsPage.vue

- Получает текущий курс доллара через API `/exchange-rate/`
- Отображает цену в KZT (либо из API, либо вычисляет на основе курса)
- Функция `getProductPriceKzt()` обеспечивает корректное отображение

### 3. ProductDetailPage.vue

- Получает текущий курс доллара при загрузке страницы
- Отображает цену товара в KZT
- Функция `getProductPriceKzt()` обеспечивает fallback расчет если нет данных от API

## Как использовать

### Изменить курс доллара

В админ-панели достаточно изменить переменную окружения:

```bash
USD_TO_KZT_RATE=480
```

Или в `docker-compose.yml`:

```yaml
environment:
  - USD_TO_KZT_RATE=480
```

### Добавить новый товар

1. В админ-панели перейти "Добавить товар"
2. Ввести цену в USD (например, 500)
3. Сразу же будет показан preview конвертированной цены в тенге (≈ 230,000 ₸)
4. Сохранить товар

### Редактировать цену товара

1. Перейти на страницу редактирования товара
2. Изменить цену в USD
3. Посмотреть preview в тенге
4. Сохранить изменения

На публичной странице товара и каталоге цена будет автоматически отображена в KZT.

## API

### GET /api/exchange-rate/

Получить текущий курс обмена USD → KZT

**Response:**

```json
{
  "rate": 460.0,
  "currency_from": "USD",
  "currency_to": "KZT"
}
```

### GET /api/products/

Список товаров с ценами

**Response:**

```json
{
  "results": [
    {
      "id": 1,
      "name": "Товар",
      "price_usd": 100.5,
      "price_kzt": 46230.0,
      "main_image": "...",
      "category_name": "Категория",
      "category": 1
    }
  ]
}
```

### GET /api/products/{id}/

Детали товара

**Response:**

```json
{
  "id": 1,
  "name": "Товар",
  "description": "Описание",
  "price_usd": 100.50,
  "price_kzt": 46230.0,
  "category": 1,
  "category_name": "Категория",
  ...
}
```

## Миграция существующих данных

После развертывания необходимо:

1. **Применить миграцию базы данных:**

   ```bash
   python manage.py migrate
   ```

2. **Если у вас уже есть товары с ценами в KZT:**
   - Создайте скрипт для конвертации: `price_usd = price_kzt / 460`
   - Запустите скрипт через Django shell или создайте data migration

## Примечания

- Курс обновляется через переменную окружения, для автоматического обновления курса через API можно расширить функционал
- Цена вычисляется на лету (в serializers), поэтому изменение курса применяется сразу
- На фронтенде добавлена поддержка fallback'а, если API не вернул `price_kzt`
