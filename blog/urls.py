from django.urls import path

from . import views

urlpatterns = [
    path("", views.BlogListView.as_view(), name="list"),
    path("<int:pk>/", views.BlogDetailView.as_view(), name="detail"),
    path("create/", views.BlogCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.BlogUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.BlogDeleteView.as_view(), name="delete"),
    path("drafts/", views.DraftListView.as_view(), name="drafts"),
]
