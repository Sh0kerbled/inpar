from api.models import Product
from django.conf import settings

print("=" * 60)
print("Скрипт конвертации цен из KZT в USD")
print("=" * 60)

exchange_rate = settings.USD_TO_KZT_RATE
print(f"\nТекущий курс: 1 USD = {exchange_rate} KZT")

products = Product.objects.all()
print(f"\nНайдено товаров: {products.count()}")

if products.count() > 0:
    print("\nПримеры существующих цен:")
    for product in products[:3]:
        print(f"  - {product.name}: ${product.price_usd}")
    
    print("\n" + "=" * 60)
    print("Товары готовы к использованию с новой системой ценообразования!")
    print("=" * 60)
else:
    print("\nНет существующих товаров в базе данных.")

print("\nПримечание:")
print("- Все цены хранятся в USD (price_usd)")
print("- При отображении автоматически конвертируются в KZT")
print("- Изменить курс можно через переменную окружения USD_TO_KZT_RATE")
