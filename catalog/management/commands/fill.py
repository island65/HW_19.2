import json

from django.core.management import BaseCommand

from catalog.models import Products, Category


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('category_data.json', encoding='utf8') as file:
            result = json.load(file)
            commands_list = []
            for item in result:
                commands_list.append(item)
            return commands_list
        # Здесь мы получаем данные из фикстуры с категориями

    @staticmethod
    def json_read_products():
        with open('products_data.json', encoding='utf8') as file:
            result = json.load(file)
            commands_list = []
            for item in result:
                commands_list.append(item)
            return commands_list
        # Здесь мы получаем данные из фикстуры с продуктами

    def handle(self, *args, **options):
        Products.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(id=category['pk'], name=category['fields']['name'],
                         description=category['fields']['description'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(
                Products(id=product['pk'], category=Category.objects.get(pk=product['fields']['category']),
                         name=product['fields']['name'], price=product['fields']['price'],
                         description=product['fields']['description']))
        # получаем категорию из базы данных для корректной связки объектов

        # Создаем объекты в базе с помощью метода bulk_create()
        Products.objects.bulk_create(product_for_create)
