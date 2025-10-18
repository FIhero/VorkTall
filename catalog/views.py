from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden, request
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from blog.models import Post

from .forms import ProductForm
from .models import Category, Product
from .services import get_products_by_category


class HomeView(TemplateView):
    """Контролер главной страницы"""

    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs):
        """Добавляет контента на главную страницу"""
        context = super().get_context_data(**kwargs)
        context["latest_products"] = Product.objects.all().order_by("-id")[:6]
        context["products"] = Product.objects.all()
        context["latest_posts"] = Post.objects.filter(is_published=True).order_by(
            "-created_at"
        )[:3]
        return context


class ContactView(TemplateView):
    """Контролер страницы контактов"""

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        """Данные для страницы контакта"""
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        """Обработка POST-запросов"""
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print(f"Новое сообщение от {name} ({email}): {message}")
        messages.success(request, "Сообщение отправлено")

        return self.get(request, *args, **kwargs)


class CatalogView(TemplateView):
    """Контролер страницы каталога"""

    template_name = "catalog/catalog.html"

    def get_context_data(self, **kwargs):
        """Добавляет информацию о категориях"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class CategoryView(ListView):
    """Контролер страницы категории"""

    model = Product
    template_name = "catalog/category.html"
    context_object_name = "products"
    paginate_by = 18

    def get_queryset(self):
        """Фильтрует товары по категориям используя сервисную функцию"""
        category_id = self.kwargs.get("category_id") or self.request.GET.get("category")

        if category_id:
            return get_products_by_category(category_id)
        else:
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        """Добавляет дополнительные данные в шаблон"""
        context = super().get_context_data(**kwargs)

        category_id = self.kwargs.get("category_id") or self.request.GET.get("category")

        context["categories"] = Category.objects.all()
        context["selected_category"] = category_id

        if category_id:
            try:
                context["selected_category_object"] = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                context["selected_category_object"] = None
                messages.error(self.request, "Категория не найдена")
        else:
            context["selected_category_object"] = None

        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    """Контролер детальной страницы товара"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        """Добавляет контент по продукту"""
        context = super().get_context_data(**kwargs)

        product = self.object

        context["related_products"] = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]

        return context

    def get_object(self, queryset=None):
        """Обработка отсутствующего товара"""
        try:
            return super().get_object(queryset)
        except Product.DoesNotExist:
            raise Http404


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Инициализирует страницу для создания продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/form.html"

    def get_success_url(self):
        """После создания переходим на страницу созданного товара"""
        return f"/products/{self.object.pk}/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Товар создан!")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Инициализирует страницу для обновления продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_success_url(self):
        """После редактирования перемещает на измененный продукт"""
        return f"/products/{self.object.pk}/"

    def form_valid(self, form):
        """Проверка прав перед редактированием"""
        product = self.get_object()

        if self.request.user != product.owner:
            return HttpResponseForbidden("Вы можете редактировать только свои товары")

        if "is_published" in form.changed_data:
            if form.cleaned_data["is_published"] is False:
                if not self.request.user.has_perm("catalog.can_unpublish_product"):
                    return HttpResponseForbidden(
                        "У вас нет прав на снятие с публикации"
                    )

        messages.success(self.request, "Товар обновлен!")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user != product.owner:
            return HttpResponseForbidden("Вы можете редактировать только свои товары")
        return super().get(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Инициализирует страницу для удаления продукта"""

    model = Product
    template_name = "catalog/confirm_delete.html"
    success_url = "/"

    def form_valid(self, form):
        """Проверка прав перед удалением"""
        product = self.get_object()

        if not (
            self.request.user == product.owner
            or self.request.user.has_perm("catalog.delete_product")
        ):
            return HttpResponseForbidden("Нет прав для удаления")

        messages.success(self.request, "Товар удален!")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if not (
            request.user == product.owner
            or request.user.has_perm("catalog.delete_product")
        ):
            return HttpResponseForbidden("Нет прав для удаления этого товара")
        return super().get(request, *args, **kwargs)
