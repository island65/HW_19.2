from django.core.cache import cache

from catalog.models import Category, Products
from config.settings import CACHE_ENABLED


def get_category_from_cache():
    """ Получает данные о категориям из кэша, если кэш пуст, получает данные БД"""
    if not CACHE_ENABLED:
        return Category.objects.all()
    categories = Category.objects.all()
    for category in categories:
        key = f'context_data_{Category.objects.get(pk=category.pk)}'
        categories = cache.get(key)
        if categories is not None:
            return categories
        categories = Category.objects.all()
        cache.set(key, categories)
    return categories


def get_products_from_cache():
    """ Получает данные о категориям из кэша, если кэш пуст, получает данные БД"""
    if not CACHE_ENABLED:
        return Products.objects.all()
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Products.objects.all()
    cache.set(key, products)
    return products
