# Frontend Integration Guide

## Setup Backend для Frontend

### 1. Поднять Backend в Docker

```bash
cd /Users/dauren/projects/inpar
docker-compose up -d
```

Контейнеры:

- `inpar_db` - PostgreSQL база данных
- `inpar_backend` - Django приложение (http://localhost:8000)
- `inpar_nginx` - Nginx (http://localhost:80)

### 2. Создать суперпользователя для админа

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 3. Получить доступ к админ панели

```
http://localhost:8000/admin/
```

### 4. Добавить тестовые данные

В админ панели:

1. Создать категории (Categories)
2. Создать товары (Products)
3. Загрузить изображения товаров (Product Images)
4. Добавить характеристики (Product Characteristics)

---

## Frontend API Calls Examples

### Vue 3 + Axios Setup

```javascript
// api.js
import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
```

### ✨ Получить все товары с поиском, фильтром и сортировкой

```javascript
import api from "@/api";

async function getProducts(filters = {}) {
  const {
    category, // категория ID
    search, // поиск по названию и описанию
    ordering, // сортировка: price, -price, name, -created_at
    price_min, // минимальная цена
    price_max, // максимальная цена
  } = filters;

  const params = new URLSearchParams();
  if (category) params.append("category", category);
  if (search) params.append("search", search);
  if (ordering) params.append("ordering", ordering);
  if (price_min) params.append("price_min", price_min);
  if (price_max) params.append("price_max", price_max);

  const response = await api.get(`/products/?${params.toString()}`);
  return response.data;
}

// Примеры использования:
await getProducts(); // все товары
await getProducts({ search: "laptop" }); // поиск
await getProducts({ category: 1 }); // по категории
await getProducts({ ordering: "price" }); // сортировка дешевые
await getProducts({ ordering: "-price" }); // сортировка дорогие
await getProducts({ search: "mouse", category: 1 }); // комбинированный фильтр
await getProducts({ price_min: 50, price_max: 500 }); // по цене
```

### Получить детали товара

```javascript
async function getProductDetail(productId) {
  const response = await api.get(`/products/${productId}/`);
  return response.data;
}

// Вернёт:
// {
//   id, name, description, price, category, category_name,
//   main_image, stock_quantity,
//   images: [...],           // все изображения
//   characteristics: [...]   // все характеристики
// }
```

### Получить категории

```javascript
async function getCategories() {
  const response = await api.get("/categories/");
  return response.data;
}
```

### Получить диапазон цен

```javascript
async function getPriceRange() {
  const response = await api.get("/products/price_range/");
  return response.data;
  // { min_price: 19.99, max_price: 1299.99 }
}
```

### Создать заказ

```javascript
async function createOrder(orderData) {
  const response = await api.post("/orders/", {
    product: orderData.productId,
    customer_name: orderData.name,
    customer_email: orderData.email,
    customer_phone: orderData.phone,
    customer_message: orderData.message,
    quantity: orderData.quantity || 1,
  });
  return response.data;
}
```

---

## Example Vue Components

### ProductList.vue (с поиском и фильтрацией)

```vue
<template>
  <div class="products">
    <!-- Поиск -->
    <div class="search-section">
      <input
        v-model="searchQuery"
        @input="handleSearch"
        placeholder="Поиск товара..."
        class="search-input"
      />
    </div>

    <!-- Фильтры -->
    <div class="filters">
      <select v-model="selectedCategory" @change="loadProducts">
        <option value="">Все категории</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </option>
      </select>

      <input
        v-model.number="priceMin"
        type="number"
        placeholder="От"
        @change="loadProducts"
      />

      <input
        v-model.number="priceMax"
        type="number"
        placeholder="До"
        @change="loadProducts"
      />

      <select v-model="sortBy" @change="loadProducts">
        <option value="-created_at">Новые</option>
        <option value="price">Дешевые</option>
        <option value="-price">Дорогие</option>
        <option value="name">По названию</option>
      </select>
    </div>

    <!-- Список товаров -->
    <div class="products-grid">
      <div
        v-for="product in products"
        :key="product.id"
        class="product-card"
        @click="goToProduct(product.id)"
      >
        <img :src="product.main_image" :alt="product.name" />
        <h3>{{ product.name }}</h3>
        <p class="price">{{ product.price }} ₽</p>
        <p class="category">{{ product.category_name }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      products: [],
      categories: [],
      searchQuery: "",
      selectedCategory: "",
      priceMin: 0,
      priceMax: 100000,
      sortBy: "-created_at",
      searchTimeout: null,
    };
  },
  mounted() {
    this.loadCategories();
    this.loadProducts();
  },
  methods: {
    async loadProducts() {
      const params = new URLSearchParams();
      if (this.selectedCategory)
        params.append("category", this.selectedCategory);
      if (this.searchQuery) params.append("search", this.searchQuery);
      if (this.priceMin) params.append("price_min", this.priceMin);
      if (this.priceMax) params.append("price_max", this.priceMax);
      params.append("ordering", this.sortBy);

      const response = await api.get(`/products/?${params.toString()}`);
      this.products = response.data;
    },

    async loadCategories() {
      const response = await api.get("/categories/");
      this.categories = response.data;
    },

    async handleSearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.loadProducts();
      }, 300);
    },

    goToProduct(productId) {
      this.$router.push(`/product/${productId}`);
    },
  },
};
</script>

<style scoped>
.products {
  padding: 20px;
}

.search-section {
  margin-bottom: 30px;
}

.search-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  max-width: 500px;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.filters select,
.filters input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.product-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  background: #f0f0f0;
}

.product-card h3 {
  padding: 10px;
  margin: 0;
}

.price {
  padding: 0 10px;
  font-weight: bold;
  color: #27ae60;
}

.category {
  padding: 0 10px 10px;
  color: #7f8c8d;
  font-size: 12px;
}
</style>
```

### ProductDetail.vue

```vue
<template>
  <div v-if="product" class="product-detail">
    <!-- Галерея изображений -->
    <div class="gallery">
      <div class="main-image">
        <img :src="currentImage || product.main_image" :alt="product.name" />
      </div>
      <div v-if="product.images" class="thumbnails">
        <img
          v-for="img in product.images"
          :key="img.id"
          :src="img.image"
          @click="currentImage = img.image"
          :class="{ active: currentImage === img.image }"
        />
      </div>
    </div>

    <!-- Информация -->
    <div class="info">
      <h1>{{ product.name }}</h1>
      <p class="price">{{ product.price }} ₽</p>
      <p class="category">{{ product.category_name }}</p>

      <p class="description">{{ product.description }}</p>

      <!-- Характеристики -->
      <div v-if="product.characteristics" class="characteristics">
        <h3>Характеристики:</h3>
        <table>
          <tr v-for="char in product.characteristics" :key="char.id">
            <td class="char-name">{{ char.name }}</td>
            <td class="char-value">{{ char.value }}</td>
          </tr>
        </table>
      </div>

      <!-- Форма заказа -->
      <form @submit.prevent="submitOrder" class="order-form">
        <h3>Оформить заказ</h3>

        <input
          v-model="orderForm.name"
          type="text"
          placeholder="Ваше имя"
          required
        />

        <input
          v-model="orderForm.email"
          type="email"
          placeholder="Email"
          required
        />

        <input
          v-model="orderForm.phone"
          type="tel"
          placeholder="Телефон"
          required
        />

        <textarea
          v-model="orderForm.message"
          placeholder="Сообщение..."
          rows="4"
        ></textarea>

        <button type="submit" class="submit-btn">Отправить запрос</button>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      product: null,
      currentImage: null,
      orderForm: {
        name: "",
        email: "",
        phone: "",
        message: "",
      },
    };
  },
  mounted() {
    this.loadProduct();
  },
  methods: {
    async loadProduct() {
      const productId = this.$route.params.id;
      const response = await api.get(`/products/${productId}/`);
      this.product = response.data;
      this.currentImage = response.data.main_image;
    },
    async submitOrder() {
      await api.post("/orders/", {
        product: this.product.id,
        customer_name: this.orderForm.name,
        customer_email: this.orderForm.email,
        customer_phone: this.orderForm.phone,
        customer_message: this.orderForm.message,
        quantity: 1,
      });
      alert("Спасибо! Мы свяжемся с вами в ближайшее время.");
      this.orderForm = { name: "", email: "", phone: "", message: "" };
    },
  },
};
</script>

<style scoped>
.product-detail {
  display: flex;
  gap: 40px;
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.gallery {
  flex: 1;
}

.main-image {
  margin-bottom: 20px;
}

.main-image img {
  width: 100%;
  border-radius: 8px;
}

.thumbnails {
  display: flex;
  gap: 10px;
}

.thumbnails img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
  border: 2px solid transparent;
}

.thumbnails img.active {
  border-color: #27ae60;
}

.info {
  flex: 1;
}

.price {
  font-size: 32px;
  font-weight: bold;
  color: #27ae60;
  margin: 10px 0;
}

.category {
  color: #7f8c8d;
}

.characteristics table {
  width: 100%;
  margin: 20px 0;
}

.characteristics td {
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.char-name {
  font-weight: bold;
}

.order-form {
  margin-top: 30px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}

.order-form input,
.order-form textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn:hover {
  background: #229954;
}
</style>
```

---

## CORS Setup

Если фронтенд на другом адресе, обновите `docker-compose.yml`:

```yaml
environment:
  - CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,http://yourfrontend.com
```

Затем перезапустите контейнер:

```bash
docker-compose restart backend
```

---

## API Query Examples

### Поиск

```
GET /api/products/?search=laptop
```

### По категории

```
GET /api/products/?category=1
```

### Фильтр по цене

```
GET /api/products/?price_min=100&price_max=500
```

### Сортировка

```
GET /api/products/?ordering=price        # дешевые
GET /api/products/?ordering=-price       # дорогие
GET /api/products/?ordering=name         # по названию
GET /api/products/?ordering=-created_at  # новые
```

### Комбинированные фильтры

```
GET /api/products/?category=1&search=mouse&ordering=price
```

---

## Troubleshooting

### Backend не запускается

```bash
docker-compose logs backend
```

### Ошибка БД

```bash
docker-compose restart db
docker-compose restart backend
```

### Очистить данные и перестартовать

```bash
docker-compose down -v
docker-compose up -d
```

### Добавить тестовые данные

```bash
cd /Users/dauren/projects/inpar
bash add_sample_data.sh
```

---

## Next Steps

1. ✅ Backend ready с полной API
2. 🎨 Build frontend с Vue 3
3. 📦 Add more features as needed
4. 🚀 Deploy to production

Happy coding! 🎉
