from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PostForm
from .models import Post


class BlogListView(ListView):
    """Инициализирует список тем блога"""

    model = Post
    template_name = "blog/list.html"
    paginate_by = 6
    context_object_name = "post_list"

    def get_queryset(self):
        """Добавляет контент в блог"""
        return Post.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Показывает детали выбранного блога"""

    model = Post
    template_name = "blog/detail.html"

    def get_object(self, queryset=None):
        """Показывает информацию выбранной статьи"""
        try:
            obj = super().get_object(queryset)
            session_key = f"post_viewed_{obj.pk}"

            if not self.request.session.get(session_key, False):
                obj.views_count += 1
                obj.save()
                self.request.session[session_key] = True

            return obj

        except Post.DoesNotExist:
            raise Http404("Статья не найдена")


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Инициализирует страницу для создания статьи"""

    model = Post
    form_class = PostForm
    template_name = "blog/form.html"
    success_url = "/blogs/"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Пост создан!")
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """Инициализирует страницу для обновления статьи"""

    model = Post
    form_class = PostForm
    template_name = "blog/form.html"

    def get_success_url(self):
        """После редактирования перемещает на измененную статью"""
        return f"/blogs/{self.object.pk}/"

    def form_valid(self, form):
        """Проверка прав перед редактированием"""
        post = self.get_object()

        if self.request.user != post.owner:
            return HttpResponseForbidden("Вы можете редактировать только свои статьи")

        if "is_published" in form.changed_data:
            if form.cleaned_data["is_published"] is False:
                if not self.request.user.has_perm("blog.can_unpublish_post"):
                    return HttpResponseForbidden(
                        "У вас нет прав на снятие с публикации"
                    )

        messages.success(self.request, "Пост обновлен!")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.owner:
            return HttpResponseForbidden("Вы можете редактировать только свои посты")
        return super().get(request, *args, **kwargs)


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """Инициализирует страницу для удаления статьи"""

    model = Post
    template_name = "blog/confirm_delete.html"
    success_url = "/blogs/"

    def form_valid(self, form):
        """Проверка прав перед удалением"""
        post = self.get_object()

        if not (
            self.request.user == post.owner
            or self.request.user.has_perm("blog.delete_post")
        ):
            return HttpResponseForbidden("Нет прав для удаления")

        messages.success(self.request, "Пост удален!")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if not (
            request.user == post.owner or request.user.has_perm("blog.delete_post")
        ):
            return HttpResponseForbidden("Нет прав для удаления этой статьи")
        return super().get(request, *args, **kwargs)


class DraftListView(LoginRequiredMixin, ListView):
    """Список черновиков"""

    model = Post
    template_name = "blog/drafts.html"
    context_object_name = "post_list"

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user, is_published=False)
