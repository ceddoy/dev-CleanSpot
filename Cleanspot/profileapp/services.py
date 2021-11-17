from authapp.models import CleanspotUser


def get_user(email):
    user = CleanspotUser.objects.get(email=email)
    return user
