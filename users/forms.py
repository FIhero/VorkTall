from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        label="Пароль",
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        }),
        label="Подтвердите пароль",
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].error_messages = {
            'required': 'Поле Email обязательно для заполнения',
            'invalid': 'Введите корректный email адрес',
            'unique': 'Пользователь с таким Email уже существует'
        }
        self.fields['first_name'].error_messages = {
            'required': 'Поле Имя обязательно для заполнения'
        }
        self.fields['last_name'].error_messages = {
            'required': 'Поле Фамилия обязательно для заполнения'
        }

        for field_name, field in self.fields.items():
            if hasattr(field, 'widget') and hasattr(field.widget, 'attrs'):
                if field_name not in ['password1', 'password2']:
                    field.widget.attrs.update({
                        'class': 'form-control',
                        'placeholder': f'Введите {field.label.lower()}'
                    })

    def clean_password2(self):
        """Проверка на соответствие паролей"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        """Сохраняет пользователя с хэшированным паролем"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля """

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'country', 'avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].label = ''
        self.fields['avatar'].help_text = ''


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль'
        })
    )

    error_messages = {
        'invalid_login': "Неверный email или пароль. Оба поля чувствительны к регистру.",
        'inactive': "Этот аккаунт неактивен.",
    }
