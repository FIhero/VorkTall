from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from catalog.models import Category, Product


def home(request):
    """Контролер главной страницы"""
    latest_products = Product.objects.all().order_by('-id')[:6]
    all_products = Product.objects.all()
    return render(request, "catalog/home.html", {
        'latest_products': latest_products,
        'products': all_products
    })

def contacts(request):
    """Контролер страницы контактов"""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print(f"Новое сообщение от {name} ({email}): {message}")

        messages.success(request, "Сообщение отправлено")
        return redirect("contacts")

    return render(request, "catalog/contacts.html")


def catalog(request):
    """Контролер страницы каталога"""
    categories = Category.objects.all()
    return render(request, 'catalog/catalog.html', {'categories': categories})


def category(request):
    """Контролер страницы категории"""
    category_id = request.GET.get('category')
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
        selected_category_object = Category.objects.get(id=category_id)
    else:
        products = Product.objects.all()
        selected_category_object = None

    paginator = Paginator(products, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/category.html', {
        'page_obj': page_obj,
        'selected_category': category_id,
        'selected_category_object': selected_category_object,
        'categories': categories,
        'products': products
    })


def product_detail(request, pk):
    """Контролер детальной страницы товара"""
    try:
        product = Product.objects.get(pk=pk)
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    except Product.DoesNotExist:
        return render(request, '404.html', status=404)

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related_products
    })
