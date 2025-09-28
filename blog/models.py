from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    preview = models.ImageField(upload_to="blog/", blank=True, null=True)
    authors = models.CharField(
        max_length=500, default="Антон", help_text="Перечисляйте авторов через запятую"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_authors_list(self):
        """Разбивает строку авторов на список"""
        return [author.strip() for author in self.authors.split(",")]
