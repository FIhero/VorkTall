import os

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import UserProfileForm, UserRegistrationForm, CustomAuthenticationForm
from .models import User


class CustomLoginView(LoginView):
    """Инициализирует страницу входа"""
    template_name = "users/login.html"
    form_class = CustomAuthenticationForm
    success_url = '/'


class RegisterView(CreateView):
    """Регистрация нового пользователя"""

    model = User
    form_class = UserRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        """Отправка приветственного письма после регистрации"""
        response = super().form_valid(form)
        send_mail(
            'Добро пожаловать в Aivova!',
            'Спасибо за регистрацию в нашем магазине.',
            os.getenv("EMAIL_HOST_USER"),
            [self.object.email],
            fail_silently=False,
        )
        return response


class AccountDetailView(DetailView):
    """Показывает детали пользователя"""

    model = User
    template_name = "users/user_detail.html"

    def get_object(self, queryset=None):
        """Показывает информацию пользователя"""
        try:
            return super().get_object(queryset)
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")


class AccountUpdateView(UpdateView):
    """Инициализирует страницу для обновления информации о пользователи"""

    model = User
    form_class = UserProfileForm
    template_name = "users/user_form.html"

    def get_success_url(self):
        """После редактирования перемещает на измененную страницу пользователя"""
        return reverse_lazy('user_detail', kwargs={'pk': self.object.pk})


class AccountDeleteView(DeleteView):
    """Инициализирует страницу для удаления пользователя"""

    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("home")
