from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from blog.models import Post
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Fill database with test data"

    def handle(self, *args, **options):
        self.stdout.write("Starting database population...")

        User = get_user_model()

        user_fields = [f.name for f in User._meta.get_fields()]
        self.stdout.write(f"Available user fields: {user_fields}")

        try:
            test_user, created = User.objects.get_or_create(
                email='test@example.com',
                defaults={
                    'first_name': 'Test',
                    'last_name': 'User',
                    'is_active': True
                }
            )

            if created:
                test_user.set_password('testpass123')
                test_user.save()
                self.stdout.write("Создан тестовый пользователь 'test@example.com'")
            else:
                self.stdout.write("Используем существующего пользователя 'test@example.com'")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка при создании пользователя: {e}")
            )
            test_user = User.objects.create(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                is_active=True
            )
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write("Создан тестовый пользователь через create")

        product_moderators_group, created = Group.objects.get_or_create(name='Модераторы продуктов')

        product_content_type = ContentType.objects.get_for_model(Product)

        try:
            view_product_perm = Permission.objects.get(
                codename='view_product',
                content_type=product_content_type
            )
            change_product_perm = Permission.objects.get(
                codename='change_product',
                content_type=product_content_type
            )
            delete_product_perm = Permission.objects.get(
                codename='delete_product',
                content_type=product_content_type
            )

            product_moderators_group.permissions.clear()
            product_moderators_group.permissions.add(
                view_product_perm,
                change_product_perm,
                delete_product_perm
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Группа 'Модераторы продуктов' создана с {product_moderators_group.permissions.count()} разрешениями"
                )
            )
        except Permission.DoesNotExist as e:
            self.stdout.write(
                self.style.ERROR(f"Права для продуктов не найдены: {e}")
            )

        content_managers_group, created = Group.objects.get_or_create(name='Контент-менеджеры')

        try:
            blog_content_type = ContentType.objects.get_for_model(Post)

            view_blog_perm = Permission.objects.get(
                codename='view_post',
                content_type=blog_content_type
            )
            add_blog_perm = Permission.objects.get(
                codename='add_post',
                content_type=blog_content_type
            )
            change_blog_perm = Permission.objects.get(
                codename='change_post',
                content_type=blog_content_type
            )
            delete_blog_perm = Permission.objects.get(
                codename='delete_post',
                content_type=blog_content_type
            )

            content_managers_group.permissions.clear()
            content_managers_group.permissions.add(
                view_blog_perm,
                add_blog_perm,
                change_blog_perm,
                delete_blog_perm
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "Группа 'Контент-менеджеры' создана с правами на управление блогом"
                )
            )

        except Permission.DoesNotExist as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Права для модели блога не найдены: {e}"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Ошибка при настройке прав для блога: {e}"
                )
            )

        try:
            unpublish_perm, created = Permission.objects.get_or_create(
                codename='can_unpublish_product',
                name='Can unpublish product',
                content_type=product_content_type
            )

            if created:
                self.stdout.write("Создано кастомное право 'can_unpublish_product'")
            else:
                self.stdout.write("Кастомное право 'can_unpublish_product' уже существует")

            product_moderators_group.permissions.add(unpublish_perm)
            self.stdout.write("Право 'can_unpublish_product' добавлено модераторам продуктов")

        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f"Не удалось добавить право can_unpublish_product: {e}")
            )

        Product.objects.all().delete()
        Category.objects.all().delete()

        category1 = Category.objects.create(
            name="Настолки",
            description="Настольные игры"
        )
        category2 = Category.objects.create(
            name="Фигурки",
            description="Коллекционные фигурки"
        )

        try:
            Product.objects.create(
                name="Монополия",
                price=2500,
                category=category1,
                owner=test_user
            )
            Product.objects.create(
                name="Дракон",
                price=3500,
                category=category2,
                owner=test_user
            )
            self.stdout.write("Тестовые продукты созданы успешно")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка при создании продуктов: {e}")
            )
            try:
                product1 = Product(
                    name="Монополия",
                    price=2500,
                    category=category1,
                    owner=test_user
                )
                product1.save()

                product2 = Product(
                    name="Дракон",
                    price=3500,
                    category=category2,
                    owner=test_user
                )
                product2.save()
                self.stdout.write("Тестовые продукты созданы через альтернативный метод")
            except Exception as e2:
                self.stdout.write(
                    self.style.ERROR(f"Критическая ошибка при создании продуктов: {e2}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Database filled successfully with groups, permissions and test data!"
            )
        )