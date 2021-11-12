from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from authapp.forms import CleanspotUserRegisterForm, CleanspotUserLoginForm
from django.urls import reverse
from django.contrib import auth
from authapp.models import CleanspotUser

from authapp.services import send_verify_email, is_activation_key_expired


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

def register(request):
    if request.method == "POST":
        register_form = CleanspotUserRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            send_verify_email(user)
            return HttpResponseRedirect(reverse('auth:registration_complete'))
    else:
        register_form = CleanspotUserRegisterForm()
    content = {
        'register_form': register_form,
    }
    return render(request, 'authapp/login1.html', content)


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
    title = 'Cброс пароля'
    if request.method == 'POST':
        reset_pass_form = PasswordResetForm(request.POST)
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

    reset_pass_form = PasswordResetForm()
    context = {
        'title': title,
        "reset_pass_form": reset_pass_form
    }
    return render(request, 'authapp/password_reset_form.html', context)
