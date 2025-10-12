import os

from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        error_messages = {
            "name": {
                "required": "Название товара обязательно для заполнения",
                "max_length": "Название не может превышать 100 символов",
            },
            "description": {
                "required": "Описание товара обязательно для заполнения",
            },
            "price": {
                "required": "Укажите цену товара",
                "invalid": "Введите корректную цену",
                "max_digits": "Цена не может превышать 10 цифр",
                "max_decimal_places": "Цена может содержать не более 2 знаков после запятой",
                "max_whole_digits": "Слишком большое значение цены",
            },
            "category": {
                "required": "Выберите категорию товара",
            },
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["name"].error_messages = {
                "required": "Название товара обязательно"
            }
            self.fields["description"].error_messages = {
                "required": "Описание товара обязательно"
            }
            self.fields["price"].error_messages = {
                "required": "Укажите цену товара",
                "invalid": "Введите корректную цену",
            }
            self.fields["category"].error_messages = {
                "required": "Выберите категорию товара"
            }

    def clean_name(self):
        """Валидация названия продукта"""
        name = self.cleaned_data["name"]
        if len(name) < 2:
            raise forms.ValidationError("Название должно содержать минимум 2 символа")
        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in forbidden_words:
            if word in name.lower():
                raise forms.ValidationError(
                    f"Название содержит запрещенное слово: {word}"
                )

        return name

    def clean_description(self):
        """Валидация описания"""
        description = self.cleaned_data["description"]
        if len(description) > 500:
            raise forms.ValidationError("Описание не должно быть длиннее 500 символов")

        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]

        for word in forbidden_words:
            if word in description.lower():
                raise forms.ValidationError(
                    f"Название содержит запрещенное слово: {word}"
                )

        return description

    def clean_image(self):
        """Валидация формата изображения"""
        image = self.cleaned_data.get("image")
        valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]

        if not image or image == "":
            return image

        if isinstance(image, str):
            return None

        ext = os.path.splitext(image.name)[1].lower()

        if ext not in valid_extensions:
            raise forms.ValidationError("Поддерживаются форматы: JPG, JPEG, PNG, GIF")

        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Размер файла не должен превышать 5MB")

        return image

    def clean_price(self):
        """Валидация цены"""
        price = self.cleaned_data["price"]

        max_price = 10**8 - 0.01
        if price > max_price:
            raise forms.ValidationError(
                f"Максимальная цена: {max_price:,.2f} руб".replace(",", " ")
            )
        return price
