from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from authapp.models import CleanspotUser, Cities, CleanspotUserType
from mainapp.models import Premises


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
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'cabinet-form__input',
                                                                                'placeholder': 'Пароль', 'type': 'password'}))
    email = forms.CharField(max_length=128, widget=forms.EmailInput(attrs={'class': 'cabinet-form__input', 'type': 'email',
                                                                          'placeholder': 'E-mail'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'cabinet-form__input',
                                                                  'type': 'tel', 'placeholder': 'Телефон'}), required=False)
    title = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'cabinet-form__input', 'type': 'text',
                                                                          'placeholder': 'Наименование'}), required=False)
    name_display_site = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'cabinet-form__input', 'type': 'text',
                                                                          'placeholder': 'Имя отображения на сайте'}), required=False)
    inn_kpp = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'cabinet-form__input', 'type': 'text',
                                                                          'placeholder': 'ИНН/КПП'}), required=False)
    city = forms.ModelChoiceField(queryset=Cities.objects.all(),
                                  widget=forms.Select(attrs={'class': 'cabinet-form__input',
                                                             'placeholder': 'Город'}),
                                  empty_label='Выберите город', required=False)

    class Meta:
        model = CleanspotUser
        fields = ('user_type', 'title', 'name_display_site', 'phone_number', 'email', 'inn_kpp', 'city', 'password')
        widgets = {'user_type': forms.HiddenInput}

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
    password = ReadOnlyPasswordHashField(widget=forms.PasswordInput(attrs={'class': 'cabinet-form__input',
                                                                           'placeholder': 'пароль'}))


class EditUsersForm(EditCleanerForm):
    user_type = forms.ModelChoiceField(queryset=CleanspotUserType.objects.all().exclude(name='Moderator').
                                       exclude(name='Cleaner'), widget=forms.Select(attrs={
                                        'class': 'cabinet-form__input'}),
                                       empty_label='Выберите тип пользователя')


class CleanspotUserAddOrEditPremise(forms.ModelForm):

    class Meta:
        model = Premises
        fields = ('premises_owner', 'premises_type', 'premises_city', 'premises_street', 'premises_house_num',
                  'premises_apartment', 'premises_intercom', 'premises_entrance', 'premises_floor')
        widgets = {'premises_owner': forms.HiddenInput}
