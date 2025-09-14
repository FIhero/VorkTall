from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Fill database with test data'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category1 = Category.objects.create(name="Настолки", description="Настольные игры")
        category2 = Category.objects.create(name="Фигурки", description="Коллекционные фигурки")

        Product.objects.create(name="Монополия", price=2500, category=category1)
        Product.objects.create(name="Дракон", price=3500, category=category2)

        self.stdout.write(self.style.SUCCESS('Database filled successfully!'))