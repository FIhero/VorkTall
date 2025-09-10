from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    """Контролер главной страницы"""
    return render(request, 'catalog/home.html')


def contacts(request):
    """Контролер страницы контактов"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(f"Новое сообщение от {name} ({email}): {message}")

        messages.success(request, 'Сообщение отправлено')
        return redirect('contacts')

    return render(request, 'catalog/contacts.html')

def catalog(request):
    """Контролер страницы каталога"""
    return render(request, 'catalog/catalog.html')

def category(request):
    """Контролер страницы категории"""
    return render(request, 'catalog/category.html')

