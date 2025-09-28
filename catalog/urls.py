from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("contacts/", views.ContactView.as_view(), name="contacts"),
    path("catalog/", views.CatalogView.as_view(), name="catalog"),
    path("category/", views.CategoryView.as_view(), name="category"),
    path(
        "category/<int:category_id>/",
        views.CategoryView.as_view(),
        name="category_detail",
    ),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
]
