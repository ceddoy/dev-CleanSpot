from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.models import CleanspotUserType, CleanspotUser
from authapp.services import send_verify_email
from profileapp.forms import CleanspotUserEditForm, CleanspotUserPasswordChangeForm, AddCleanerForm, EditCleanerForm, \
    EditUsersForm
from profileapp.services import get_user


@login_required
def edit(request, email):
    title = 'личный кабинет'
    is_moder = CleanspotUser.objects.get(email=email).user_type == CleanspotUserType.objects.get(name='Moderator')
    if request.method == "POST":
        edit_form = CleanspotUserEditForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('edit:edit', args=[get_user(email)]))
    else:
        edit_form = CleanspotUserEditForm(instance=request.user)
    content = {
        'title': title,
        'edit_form': edit_form,
        'user': get_user(email),
        'is_moder': is_moder
    }
    return render(request, 'profileapp/edit.html', content)


@login_required
def change_password(request, email):
    title = 'смена пароля'
    if request.method == 'POST':
        change_pass_form = CleanspotUserPasswordChangeForm(request.user, request.POST)
        if change_pass_form.is_valid():
            change_pass_form.save()
            update_session_auth_hash(request, change_pass_form.user)
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        change_pass_form = CleanspotUserPasswordChangeForm(request.user, )

    content = {
        'title': title,
        'change_pass_form': change_pass_form,
        'user': get_user(email)
    }
    return render(request, 'profileapp/change_password.html', content)


lk_admin_menu = {
    'lk_admin_cleaner_add': ['Добавление партнера', 'edit:lk_admin_cleaner_add'],
    'lk_admin_cleaner_list': ['Редактирование партнера', 'edit:lk_admin_cleaner_list'],
    'lk_admin_history': ['История всех заказов', 'edit:lk_admin_history'],
    'lk_admin_users_list': ['Пользователи', 'edit:lk_admin_users_list'],
}


def lk_admin_cleaner_add(request, email):
    moder_pk = CleanspotUserType.objects.get(name='Cleaner').pk
    add_form = AddCleanerForm(request.POST if request.POST else None)
    if request.method == 'POST':

        if add_form.is_valid():
            user = add_form.save()
            send_verify_email(user)
            return HttpResponseRedirect(reverse('edit:lk_admin_cleaner_add', args=[get_user(email)]))

    context = {
        'form': add_form,
        'moder_pk': moder_pk,
        'lk_admin_menu': lk_admin_menu,
        'user': get_user(email)
    }
    return render(request, 'profileapp/lk_admin_add.html', context)


def lk_admin_cleaner_list(request, email):
    cleaners = CleanspotUser.objects.filter(user_type__name='Cleaner')
    context = {
        'cleaners': cleaners,
        'lk_admin_menu': lk_admin_menu,
        'user': get_user(email)
    }
    return render(request, 'profileapp/lk_admin_edit.html', context)


def lk_admin_del(request, email, pk):
    CleanspotUser.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('edit:lk_admin_cleaner_list', args=[get_user(email)]))


def lk_admin_cleaner_edit(request, email, pk):
    moder_pk = CleanspotUserType.objects.get(name='Cleaner').pk
    if request.method == 'POST':
        edit_form = EditCleanerForm(request.POST, instance=CleanspotUser.objects.get(pk=pk))
        print(edit_form)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('edit:lk_admin_cleaner_list', args=[get_user(email)]))
    else:
        edit_form = EditCleanerForm(instance=CleanspotUser.objects.get(pk=pk))

    context = {
        'form': edit_form,
        'moder_pk': moder_pk,
        'lk_admin_menu': lk_admin_menu,
        'user': get_user(email),
    }
    return render(request, 'profileapp/lk_admin_add.html', context)


def lk_admin_history(request, email):
    # TODO: Создать страницу просмотра всех заказов в ЛК администратора
    context = {
        'lk_admin_menu': lk_admin_menu,
        'user': get_user(email)
    }
    return render(request, 'profileapp/lk_admin_history.html', context)


def lk_admin_users_list(request, email):
    users = CleanspotUser.objects.all().exclude(user_type__name='Moderator').exclude(user_type__name='Cleaner')
    context = {
        'lk_admin_menu': lk_admin_menu,
        'users': users,
        'user': get_user(email)
    }
    return render(request, 'profileapp/lk_admin_users.html', context)


def lk_admin_users_del(request, email, pk):
    CleanspotUser.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('profileapp:lk_admin_users_list', args=[get_user(email)]))


def lk_admin_users_edit(request, email, pk):
    if request.method == 'POST':
        edit_form = EditUsersForm(request.POST, instance=CleanspotUser.objects.get(pk=pk))
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('profileapp:lk_admin_users_list', args=[get_user(email)]))
    else:
        edit_form = EditUsersForm(instance=CleanspotUser.objects.get(pk=pk))

    context = {
        'form': edit_form,
        'lk_admin_menu': lk_admin_menu,
        'user': get_user(email)
    }
    return render(request, 'profileapp/lk_admin_users_edit.html', context)
