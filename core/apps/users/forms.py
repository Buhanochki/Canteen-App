from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from core.apps.users.models import CustomUser


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите почту"}),
    )

    password = forms.CharField(
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
                "placeholder": "Введите пароль",
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username == "":
            return self.add_error("username", "Почта не может быть пустой")
        elif "@" not in username or "." not in username:
            return self.add_error("username", "Почта введена некоректно")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password == "":
            return self.add_error("password", "Пароль не может быть пустым")
        return password

    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            if field not in errors:
                self.fields[field].widget.attrs.update({"class": "form-control is-valid"})
            else:
                self.fields[field].widget.attrs.update({"class": "form-control is-invalid"})
        return super().is_valid()


class CustomUserMixinForm(forms.ModelForm):
    def is_valid(self):
        errors = self.errors.as_data()
        for field in self.fields:
            if field not in errors:
                self.fields[field].widget.attrs.update({"class": "form-control is-valid"})
            else:
                self.fields[field].widget.attrs.update({"class": "form-control is-invalid"})
        return super().is_valid()

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name").capitalize()
        if last_name == "":
            return self.add_error("last_name", "Введите фамилию")

        return last_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name").capitalize()
        if first_name == "":
            return self.add_error("first_name", "Введите имя")

        return first_name

    def clean_surname(self):
        surname = self.cleaned_data.get("surname").capitalize()
        if surname != "":
            self.fields["surname"].widget.attrs.update({"class": "form-control is-valid"})
        return surname

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if email == "":
            return self.add_error("email", "Введите электронную почту")

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not password1 or not password2:
            self.add_error("password2", "Введите оба пароля")
            return self.add_error("password1", "Введите оба пароля")
        elif password1 != password2:
            self.add_error("password2", "Пароли не совпадают")
            return self.add_error("password1", "Пароли не совпадают")

        return password2


class ExtendedUserCreationForm(CustomUserMixinForm, UserCreationForm):
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(ExtendedUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        self.fields["email"].widget.attrs.update(autofocus=False)

    class Meta:
        model = CustomUser
        fields = ["last_name", "first_name", "surname", "email", "status", "password1", "password2"]
        widgets = {
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Фамилия",
                }
            ),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"}),
            "surname": forms.TextInput(attrs={"class": "form-control", "placeholder": "Отчество"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Почта"}),
            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "password1": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Пароль"}
            ),
            "password2": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Повторите пароль"}
            ),
        }


class UserProfileUpdateForm(CustomUserMixinForm, UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["last_name", "first_name", "surname", "email", 'allergies']
        widgets = {
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Фамилия",
                }
            ),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"}),
            "surname": forms.TextInput(attrs={"class": "form-control", "placeholder": "Отчество"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "allergies": forms.SelectMultiple(attrs={"class": "form-control"})
        }
        exclude = ["many_to_many_field"]

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
