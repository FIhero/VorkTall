from django.core.cache import cache
from .models import Product


def get_products_by_category(category_id):
    """Сервисная функция для получения продуктов по категории с низкоуровневым кешированием"""
    cache_key = f'products_category_{category_id}'

    products = cache.get(cache_key)

    if products is None:
        print(f"Кеш пустой, загружаем из БД для категории {category_id}")

        products = Product.objects.filter(category_id=category_id)

        cache.set(cache_key, products, 60 * 15)

        print(f"Данные сохранены в кеш с ключом: {cache_key}")
    else:
        print(f"Данные загружены из кеша для категории {category_id}")

    return products