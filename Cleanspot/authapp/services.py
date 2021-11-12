import hashlib
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now


def send_verify_email(user):
    """Отвечает за отправку активационного ключа на почту/ы"""
    verify_link = reverse('auth:verify', args=[user.email, generic_activation_key(user)])
    subject = f'Подтверждение учетной записи {user.email}'
    message = f'Ссылка для активации учетной записи: {settings.BASE_URL}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)


def is_activation_key_expired(user):
    """Провека срока действия активационного ключа"""
    now_date = now() - timedelta(hours=48)
    if now_date <= user.activation_key_expires:
        return False
    return True


def generic_activation_key(user):
    """Генерация активационного ключа"""
    user.activation_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()
    user.save()
    return user.activation_key
