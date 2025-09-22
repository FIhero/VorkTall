from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("catalog/", views.catalog, name="catalog"),
    path("category/", views.category, name="category"),
    path("products/<int:pk>/", views.product_detail, name="product_detail")
]
