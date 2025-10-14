from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField("Email", max_length=254, unique=True)
    phone = models.CharField("Телефон", max_length=15, blank=True, null=True)
    country = models.CharField("Страна", max_length=50, blank=True, null=True)
    avatar = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True,
        default="users/default_user.png",
        verbose_name="Аватар",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def blog_posts(self):
        """Количество опубликованных статей пользователя"""
        from blog.models import Post

        return Post.objects.filter(owner=self, is_published=True).count()

    @property
    def blog_drafts(self):
        """Количество черновиков пользователя"""
        from blog.models import Post

        return Post.objects.filter(owner=self, is_published=False).count()

    @property
    def products_count(self):
        """Количество товаров пользователя"""
        from catalog.models import Product

        return Product.objects.filter(owner=self).count()
