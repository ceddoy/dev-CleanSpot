from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import TemplateView

from authapp.forms import CleanspotUserRegisterForm, CleanspotUserLoginForm, CleanspotPasswordResetForm, \
    CleanspotSetPasswordForm, CleanspotCleanerRegistrationForm
from django.urls import reverse
from django.contrib import auth
from authapp.models import CleanspotUser, CleanspotUserType

from authapp.services import send_verify_email, is_activation_key_expired


class AuthPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CleanspotSetPasswordForm
    title = 'Введите новый пароль'
    template_name = 'authapp/password_reset_confirm.html'
    success_url = '/auth/password_complete/'


class AuthPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'authapp/password_reset_complete.html'


class AuthTemplateView(TemplateView):
    template_name = 'authapp/register_complete.html'


class RegisterCleanerCompleteTemplateView(TemplateView):
    template_name = 'authapp/register_cleaner_complete.html'


class AuthPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'authapp/password_reset_done.html'


def login(request):
    if request.method == 'POST':
        login_form = CleanspotUserLoginForm(data=request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:main'))
    else:
        login_form = CleanspotUserLoginForm()
    content = {
        'login_form': login_form
    }
    return render(request, 'authapp/loginIndividual.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:main'))


def register_step_1(request):
    return render(request, 'authapp/register_step_1.html')


def register_step_2(request):
    user_type = {
        'company': 'Юридические лица',
        'individual': 'Физические лица',
        'cleaner': 'Cleaner'
    }
    if request.method == "POST":
        register_form = CleanspotUserRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            send_verify_email(user)
            return HttpResponseRedirect(reverse('auth:registration_complete'))
    else:
        request_type = ''
        if 'register' in request.GET and request.GET['register']:
            request_type = request.GET['register']
            if request_type == 'cleaner':
                return HttpResponseRedirect(reverse('auth:register_cleaner'))
        register_form = CleanspotUserRegisterForm(
            initial={'user_type': CleanspotUserType.objects.get(name=user_type[request_type])})
    content = {
        'register_form': register_form,
    }
    return render(request, 'authapp/register_step_2.html', content)


def register_cleaner(request):
    if request.method == 'POST':
        form = CleanspotCleanerRegistrationForm(request.POST)
        subject = 'Регистрация нового клинера'
        messages = f'Просьба связаться по регистрации нового клинера\n\nИмя: {form.data["name"]}\nТелефон: ' \
                   f'{form.data["phone_number"]}'
        email = 'krivochenko_andrey@mail.ru'
        send_mail(subject, messages, settings.EMAIL_HOST_USER, [email])
        return HttpResponseRedirect(reverse('authapp:register_cleaner_complete'))
    else:
        form = CleanspotCleanerRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'authapp/register_cleaner.html', context)


def verify(request, email, activation_key):
    user = CleanspotUser.objects.get(email=email)
    if user.activation_key == activation_key and not is_activation_key_expired(user):
        user.is_active = True
        user.activation_key = ''
        user.save()
    context = {
        'user': user
    }
    return render(request, 'authapp/verification.html', context)


def reset_password(request):
    if request.method == 'POST':
        reset_pass_form = CleanspotPasswordResetForm(request.POST)
        if reset_pass_form.is_valid():
            data = reset_pass_form.cleaned_data['email']
            try:
                user = CleanspotUser.objects.get(email=data)
                if user:
                    subject = 'Запрос на сброс пароля'
                    reset_link = reverse('auth:confirm_password', args=[urlsafe_base64_encode(force_bytes(user.pk)),
                                                                        default_token_generator.make_token(user)])

                    message = f'Ссылка на сброс пароля: {settings.BASE_URL}{reset_link}'
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)
                    return HttpResponseRedirect(reverse('auth:done_password'))
            except CleanspotUser.DoesNotExist:
                return HttpResponse('Такой почты не существует!')

    reset_pass_form = CleanspotPasswordResetForm()
    context = {
        "reset_pass_form": reset_pass_form
    }
    return render(request, 'authapp/password_reset_form.html', context)
