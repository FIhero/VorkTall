from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from .views import (AccountDeleteView, AccountDetailView, AccountUpdateView,
                    CustomLoginView, RegisterView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("<int:pk>/", AccountDetailView.as_view(), name="user_detail"),
    path("<int:pk>/edit/", AccountUpdateView.as_view(), name="user_edit"),
    path("<int:pk>/delete/", AccountDeleteView.as_view(), name="user_delete"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy('home')), name="logout")
]
