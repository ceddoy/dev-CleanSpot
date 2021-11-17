from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from authapp.models import CleanspotUser, Cities, CleanspotUserType


class CleanspotUserEditForm(UserChangeForm):
    class Meta:
        model = CleanspotUser
        fields = ('title', 'phone_number', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = forms.HiddenInput()


class CleanspotUserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CleanspotUser
        fields = ('new_password1', 'new_password2', 'old_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AddCleanerForm(forms.ModelForm):
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control mb-3',
                                                                                'placeholder': 'пароль'}))
    email = forms.CharField(max_length=128, widget=forms.EmailInput(attrs={'class': 'form-control mb-3',
                                                                           'type': 'email',
                                                                           'placeholder': 'email',
                                                                           'aria-label': 'input email'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control mb-3',
                                                                  'type': 'tel', 'placeholder': 'Телефон',
                                                                  'aria-label': 'input phone'}), required=False)
    title = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'type': 'text',
                                                                          'placeholder': 'Наименование',
                                                                          'aria-label': 'input name'}), required=False)
    name_display_site = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'form-control mb-3',
                                                                                      'type': "text",
                                                                                      'placeholder': 'Имя отображения '
                                                                                                     'на сайте',
                                                                                      'aria-label': 'input name on site'
                                                                                      }), required=False)
    inn_kpp = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'form-control mb-3',
                                                                            'type': "text",
                                                                            'placeholder': 'ИНН/КПП',
                                                                            'aria-label': 'input inn'
                                                                            }), required=False)
    city = forms.ModelChoiceField(queryset=Cities.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control mb-3',
                                                             'placeholder': 'Город'}),
                                  empty_label='Выберите город', required=False)

    class Meta:
        model = CleanspotUser
        fields = ('user_type', 'title', 'name_display_site', 'phone_number', 'email', 'inn_kpp', 'city', 'password')

    def clean_name(self):
        data = self.cleaned_data['title']

        if CleanspotUser.objects.filter(title=data).exists():
            raise ValidationError('Пользователь с таким именем уже существует')

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if data == '':
            return None
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class EditCleanerForm(AddCleanerForm):
    password = ReadOnlyPasswordHashField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3',
                                                                           'placeholder': 'пароль'}))


class EditUsersForm(EditCleanerForm):
    user_type = forms.ModelChoiceField(queryset=CleanspotUserType.objects.all().exclude(name='Moderator').
                                       exclude(name='Cleaner'), widget=forms.Select(attrs={
                                        'class': 'form-control mb-3'}),
                                       empty_label='Выберите тип пользователя')
