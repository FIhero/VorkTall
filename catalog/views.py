from django.contrib import messages
from django.http import Http404
from django.views.generic import DetailView, ListView, TemplateView

from blog.models import Post

from .models import Category, Product


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
        """Фильтрует товары по категориям"""
        queryset = Product.objects.filter()

        category_id = self.kwargs.get("category_id") or self.request.GET.get("category")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        """Добавляет дополнительные данные в шаблон"""
        context = super().get_context_data(**kwargs)

        category_id = self.kwargs.get("category_id") or self.request.GET.get("category")

        context["categories"] = Category.objects.all()
        context["selected_category"] = category_id

        if category_id:
            context["selected_category_object"] = Category.objects.get(id=category_id)

        else:
            context["selected_category_object"] = None

        return context


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
