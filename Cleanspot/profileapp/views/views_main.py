from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from authapp.models import CleanspotUserType, CleanspotUser
from authapp.services import send_verify_email
from common.menu import LK_MAIN_MENU, LK_ADMIN_MENU
from mainapp.models import Premises
from profileapp.forms import CleanspotUserEditForm, CleanspotUserPasswordChangeForm, AddCleanerForm, EditCleanerForm, \
    EditUsersForm, CleanspotUserAddOrEditPremise
from profileapp.services import get_user

lk_user_menu = {
    'lk_add_order': ['Создать заказ', 'edit:lk_add_order'],
    'lk_my_premises': ['Мои помещения', 'edit:lk_my_premises'],
    'lk_current_order': ['Текущий заказ', 'edit:lk_current_order'],
    'lk_order_history': ['История заказов', 'edit:lk_order_history'],
    'lk_my_data': ['Мои данные', 'edit:lk_my_data']
}


@login_required
def edit(request, email):
    is_moder = CleanspotUser.objects.get(email=email).user_type == CleanspotUserType.objects.get(name='Moderator')
    if request.method == "POST":
        edit_form = CleanspotUserEditForm(request.POST, instance=get_user(email))
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('edit:lk_my_data', args=[get_user(email)]))
    else:
        edit_form = CleanspotUserEditForm(instance=get_user(email))
    content = {
        'edit_form': edit_form,
        'lk_user_menu': lk_user_menu,
        'user': get_user(email),
        'is_moder': is_moder
    }
    return render(request, 'profileapp/cabinetClientData.html', content)


@login_required
def lk_add_order(request, email):
    # context = {
    #     'lk_user_menu': lk_user_menu,
    #     'user': get_user(email)
    # }
    return HttpResponseRedirect(reverse('cart:cart_main'))


@login_required
def lk_current_order(request, email):
    context = {
        'lk_user_menu': lk_user_menu,
        'user': get_user(email)
    }
    return render(request, 'profileapp/lk_current_order.html', context)


@method_decorator(login_required, name='dispatch')
class LkMyPremisesView(TemplateView):
    template_name = 'profileapp/lk_my_premises.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = kwargs['email']
        context['user'] = email
        context['lk_user_menu'] = lk_user_menu
        all_user_premises = Premises.objects.filter(premises_owner__email=email)
        context['all_user_premises'] = all_user_premises
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['add_form_premise'] = CleanspotUserAddOrEditPremise(
            initial={'premises_owner': get_user(context['user'])},
            instance=request.user,
            prefix='add_premise')
        edit_form_list = []
        for user_premises in context['all_user_premises']:
            edit_form = CleanspotUserAddOrEditPremise(
                initial={'premises_owner': get_user(context['user'])},
                prefix='edit_premise',
                instance=user_premises)
            edit_form_list.append(edit_form)
        context['edit_form_list'] = edit_form_list
        return self.render_to_response(context)

    def post(self, request, email, **kwargs):
        add_form_premise = CleanspotUserAddOrEditPremise(
            request.POST,
            prefix='add_premise')
        if add_form_premise.is_valid():
            add_form_premise.save()
            return HttpResponseRedirect(reverse('edit:lk_my_premises', args=[get_user(email)]))
        form_pk = request.POST.get('pk')
        edit_form_premise = CleanspotUserAddOrEditPremise(
            request.POST,
            instance=Premises.objects.get(pk=form_pk),
            prefix='edit_premise')
        if edit_form_premise.is_valid():
            edit_form_premise.save()
            return HttpResponseRedirect(reverse('edit:lk_my_premises', args=[get_user(email)]))
        context = self.get_context_data(**kwargs)
        context['add_form_premise'] = add_form_premise
        context['edit_form_list'] = edit_form_premise
        return self.render_to_response(context)


@login_required
def lk_my_premises_delete(request, email, pk):
    Premises.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('edit:lk_my_premises', args=[get_user(email)]))


@login_required
def lk_order_history(request, email):
    context = {
        'lk_user_menu': lk_user_menu,
        'user': get_user(email)
    }
    return render(request, 'profileapp/lk_order_history.html', context)


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


def lk_admin_cleaner_add(request, email):
    if request.method == 'POST':
        add_form = AddCleanerForm(request.POST)
        if add_form.is_valid():
            user = add_form.save()
            send_verify_email(user)
            return HttpResponseRedirect(reverse('edit:lk_admin_cleaner_add', args=[get_user(email)]))
    else:
        add_form = AddCleanerForm(initial={'user_type': CleanspotUserType.objects.get(name='Cleaner')})

    context = {
        'form': add_form,
        'lk_admin_menu': LK_ADMIN_MENU,
        'user': get_user(email),
        'lk_admin_main_menu': LK_MAIN_MENU,
    }
    return render(request, 'profileapp/lk_admin_add.html', context)


def lk_admin_cleaner_list(request, email):
    cleaners = CleanspotUser.objects.filter(user_type__name='Cleaner').order_by('title')
    paginator = Paginator(cleaners, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'lk_admin_menu': LK_ADMIN_MENU,
        'user': get_user(email),
        'lk_admin_main_menu': LK_MAIN_MENU,
        'page_obj': page_obj,
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
        'lk_admin_menu': LK_ADMIN_MENU,
        'lk_admin_main_menu': LK_MAIN_MENU,
        'user': get_user(email),
    }
    return render(request, 'profileapp/lk_admin_add.html', context)


def lk_admin_history(request, email):
    # TODO: Создать страницу просмотра всех заказов в ЛК администратора
    context = {
        'lk_admin_menu': LK_ADMIN_MENU,
        'lk_admin_main_menu': LK_MAIN_MENU,
        'user': get_user(email)
    }
    return render(request, 'profileapp/lk_admin_history.html', context)


def lk_admin_price(request, email):
    # TODO: Создать страницу с прайсом в ЛК администратора
    context = {
        'lk_admin_menu': LK_ADMIN_MENU,
        'lk_admin_main_menu': LK_MAIN_MENU,
        'user': get_user(email)
    }
    return render(request, 'profileapp/lk_admin_price.html', context)


def lk_admin_users_list(request, email):
    users = CleanspotUser.objects.all().exclude(user_type__name='Moderator').exclude(
        user_type__name='Cleaner').order_by('title')
    paginator = Paginator(users, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'lk_admin_menu': LK_ADMIN_MENU,
        'lk_admin_main_menu': LK_MAIN_MENU,
        'user': get_user(email),
        'page_obj': page_obj,
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
        'lk_admin_menu': LK_ADMIN_MENU,
        'lk_admin_main_menu': LK_MAIN_MENU,
        'user': get_user(email)
    }
    return render(request, 'profileapp/lk_admin_users_edit.html', context)
