from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Post


class BlogListView(ListView):
    """Инициализирует список тем блога"""

    model = Post
    template_name = "blog/list.html"

    def get_queryset(self):
        """Добавляет контент в блог"""
        return Post.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Показывает детали выбранного блога"""

    model = Post
    template_name = "blog/detail.html"

    def get_object(self):
        """Показывает информацию выбранной статьи"""
        obj = super().get_object()
        session_key = f"post_viewed_{obj.pk}"
        if not self.request.session.get(session_key, False):
            obj.views_count += 1
            obj.save()
            self.request.session[session_key] = True

        return obj


class BlogCreateView(CreateView):
    """Инициализирует страницу для создания статьи"""

    model = Post
    template_name = "blog/form.html"
    fields = ["title", "authors", "content", "preview", "is_published"]
    success_url = "/blogs/"


class BlogUpdateView(UpdateView):
    """Инициализирует страницу для обновления статьи"""

    model = Post
    template_name = "blog/form.html"
    fields = ["title", "authors", "content", "preview", "is_published"]

    def get_success_url(self):
        """После редактирования перемещает на измененную статью"""
        return f"/blogs/{self.object.pk}/"


class BlogDeleteView(DeleteView):
    """Инициализирует страницу для удаления статьи"""

    model = Post
    template_name = "blog/confirm_delete.html"
    success_url = "/blogs/"


class DraftListView(ListView):
    """Список черновиков"""

    model = Post
    template_name = "blog/drafts.html"
    context_object_name = "post_list"

    def get_queryset(self):
        return Post.objects.filter(is_published=False)
