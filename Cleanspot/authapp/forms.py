from django import forms
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from authapp.models import CleanspotUser


class CleanspotUserLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email*",
        max_length=128,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
                                       'class': 'login_form__input',
                                       'type': 'email',
                                       'placeholder': 'mail@mail.ru'})
    )

    password = forms.CharField(
        label="Пароль*",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'login_form__input',
                                          'type': 'password',
                                          'placeholder': 'Введите пароль'}),
    )
    error_messages = {
        'invalid_email': "Вы ввели неправильно почту/пароль. Повторите попытку!",
        'inactive': "Этот аккаунт неактивен. Проверьте свою почту, "
                    "вам должно было прийти сообщение с активационной ссылкой.",
    }

    class Meta:
        model = CleanspotUser
        fields = ('email', 'password')

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_email_error()
            else:
                self.confirm_email_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_email_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_email_error(self):
        return ValidationError(
            self.error_messages['invalid_email'],
            code='invalid_email',
        )


class CleanspotUserRegisterForm(UserCreationForm):
    phone_number = PhoneNumberField(
        required=False,
        label='Телефон',
        label_suffix=' (необязательное поле):',
        help_text='Формат ввода телефона: "79113334455"',
        widget=forms.TextInput(attrs={'class': 'form-control login_form__input',
                                      'type': 'tel',
                                      'placeholder': 'Введите телефон'})
    )

    email = forms.EmailField(
        label="Email *",
        max_length=128,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
                                       'class': 'login_form__input',
                                       'type': 'email',
                                       'placeholder': 'mail@mail.ru'})
    )

    password1 = forms.CharField(
        label="Пароль *",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'login_form__input',
                                          'type': 'password',
                                          'placeholder': 'Введите пароль'}),
    )

    password2 = forms.CharField(
        label="Повторите пароль *",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'login_form__input',
                                          'type': 'password',
                                          'placeholder': 'Введите пароль'}),
    )

    class Meta:
        model = CleanspotUser
        fields = ('user_type', 'email', 'phone_number', 'password1', 'password2')
        widgets = {'user_type': forms.HiddenInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if data == '':
            return None
        return data


class CleanspotPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email *',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email',
                                       'class': 'login_form__input',
                                       'type': 'email',
                                       'placeholder': 'mail@mail.ru'})
    )

    class Meta:
        model = CleanspotUser
        fields = ('email',)


class CleanspotSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'login_form__input',
                                          'type': 'password',
                                          'placeholder': 'Введите новый пароль'}
                                   ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'login_form__input',
                                          'type': 'password',
                                          'placeholder': 'Подтвердите новый пароль'}
                                   ),
    )


class CleanspotCleanerRegistrationForm(forms.Form):
    name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control login_form__input',
                                      'type': 'text',
                                      'placeholder': 'Как к вам обращаться?'})
    )

    phone_number = PhoneNumberField(
        label='Телефон',
        help_text='Формат ввода телефона: "79113334455"',
        widget=forms.TextInput(attrs={'class': 'form-control login_form__input',
                                      'type': 'tel',
                                      'placeholder': 'Введите телефон'})
    )
