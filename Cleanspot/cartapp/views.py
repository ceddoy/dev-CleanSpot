import calendar
import datetime
import uuid
import json

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.edit import FormView

from cartapp.forms import AddToCartForm, AddToCartWindowsForm, AddDateToCartForm

from cartapp.models import Service, ServiceType, UserTypeForServiceType, Cart, CartService, DaysOfWeek, WindowWashing
from common.const import MONTH_LIST, CLEANING_TIME_CHOICES
from orderapp.models import Order


class ShowListServicesView(FormView):
    form_class = AddToCartForm
    success_url = '/'
    cart_id = None

    def get_success_url(self):
        service_type = self.request.session['type_servise']
        if service_type == 'daily_as_scheduled':
            if self.request.user.is_authenticated:
                order = Order.objects.create(client=self.request.user, cart=Cart.objects.get(pk=self.cart_id))
            else:
                order = Order.objects.create(session_key=Cart.objects.get(pk=self.cart_id).session_key,
                                             cart=Cart.objects.get(id=self.cart_id))
            return reverse('order:order_premise', args=[order.id])
        else:
            user_type = self.kwargs['usertypeforservicetype_slug']
            return reverse('cart:date_for_cart', kwargs={'usertypeforservicetype_slug': user_type,
                                                         'servisetype_slug': service_type,
                                                         'pk': self.cart_id})

    def post(self, request, *args, **kwargs):
        """Логика обработки для анонимного юзера или для зарегистрированного"""
        form = self.get_form()
        if form.is_valid():
            services = form.cleaned_data.pop('services')
            comment = form.cleaned_data.pop('comment')
            cleaning_days = form.cleaned_data.pop('cleaning_days')
            number_stuff = form.cleaned_data.pop('number_stuff')
            clean_time = form.cleaned_data.pop('cleaning_time')
            is_windows = form.cleaned_data.pop('is_windows')
            if request.user.is_authenticated:
                cart = Cart.objects.create(owner=request.user)
                for service in services:
                    CartService.objects.create(cart=cart, service=service, user=request.user)
                    Cart.objects.get(id=cart.id).services.add(CartService.objects.get(cart=cart, service=service))
            else:
                cart = Cart.objects.create(session_key=uuid.uuid4())
                for service in services:
                    CartService.objects.create(cart=cart, service=service, session_key=cart.session_key)
                    Cart.objects.get(id=cart.id).services.add(CartService.objects.get(cart=cart, service=service))
            self.cart_id = cart.id
            if cleaning_days:
                request.session['days'] = []
                for day in cleaning_days:
                    Cart.objects.get(id=cart.id).cleaning_days.add(DaysOfWeek.objects.get(short_title=day))
                    request.session['days'].append(day.short_title)
            if number_stuff:
                request.session['number_stuff'] = number_stuff
                cart.number_stuff = number_stuff
            if comment:
                cart.comment = comment
            if clean_time:
                for time_of_day in CLEANING_TIME_CHOICES:
                    if time_of_day[0] == clean_time:
                        request.session['cleaning_time'] = time_of_day[1]
                cart.cleaning_time = clean_time
            if is_windows or \
                    ('servisetype_slug' in self.kwargs and self.kwargs['servisetype_slug'] == 'window_cleaning'):
                windows = WindowWashing.objects.create(
                    num_windows=form.data.get('Количество окон'),
                    num_window_frame=form.data.get('Количество створок окон'),
                    num_stained_windows=form.data.get('Количество витражных окон'),
                    num_stained_window_frame=form.data.get('Количество створок витражных окон'),
                    num_showcase=form.data.get('Количество витрин'),
                    square_windows=form.data.get('Площадь остекления окон'),
                    square_showcase=form.data.get('Площадь остекления витрин'),
                    height_showcase=form.data.get('Высота витрин'),
                    cart=cart
                )
                cart.windows.add(windows)
            cart.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_type = get_object_or_404(UserTypeForServiceType, slug=self.kwargs['usertypeforservicetype_slug'])
        if 'servisetype_slug' in self.kwargs:
            type_service = get_object_or_404(
                ServiceType,
                slug=self.kwargs['servisetype_slug'],
                user_type_for_service_type=user_type
            )
            kwargs['type_servise'] = self.kwargs['servisetype_slug']
        else:
            type_service = ServiceType.objects.filter(user_type_for_service_type=user_type)[0]
            kwargs['type_servise'] = type_service.name
        self.request.session['type_servise'] = kwargs['type_servise']
        kwargs['services_dict'] = Service.objects.filter(service_type__pk=type_service.pk).select_related()
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        windows_form = AddToCartWindowsForm()
        user_type = get_object_or_404(UserTypeForServiceType, slug=self.kwargs['usertypeforservicetype_slug'])
        if 'servisetype_slug' in self.kwargs:
            service_type_name = get_object_or_404(
                ServiceType,
                slug=self.kwargs['servisetype_slug'],
                user_type_for_service_type=user_type
            ).description
        else:
            service_type_name = ServiceType.objects.filter(user_type_for_service_type=user_type)[0].description
        context.update({
            'user_type_for_service_type': UserTypeForServiceType.objects.all(),
            'service_type': ServiceType.objects.filter(
                user_type_for_service_type__name='legal_person'
            ) if self.kwargs['usertypeforservicetype_slug'] == 'legal_person' else ServiceType.objects.filter(
                user_type_for_service_type__name='private_person'),
            'service_type_name': service_type_name,
            'windows_form': windows_form,
        })
        self.request.session['servise_type'] = service_type_name
        return context

    def get_template_names(self):
        user_type = self.kwargs['usertypeforservicetype_slug']
        if 'servisetype_slug' in self.kwargs:
            service_type = self.kwargs['servisetype_slug']
        else:
            service_type = ServiceType.objects.filter(user_type_for_service_type__name=user_type)[0].name
        template_name = f'cartapp/{user_type}_{service_type}.html'
        return [template_name]


class CalendarTableFormView(FormView):
    form_class = AddDateToCartForm
    template_name = 'cartapp/orderEntity-calendar-table.html'

    def get_context_data(self, **kwargs):
        context = super(CalendarTableFormView, self).get_context_data(**kwargs)
        cldr = calendar.Calendar()
        calendar_list = cldr.monthdatescalendar(int(self.kwargs['year']), int(self.kwargs['month']))
        context.update({
            'calendar': calendar_list,
            'year': int(self.kwargs['year']),
            'month': MONTH_LIST[int(self.kwargs['month'])],
            'now': datetime.datetime.now(),
        })
        return context


@csrf_exempt
def add_date_to_cart(request, *args, **kwargs):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        body = json.loads(body)
        date = datetime.date(year=int(body['year']), month=int(body['month']), day=int(body['day']))
        is_other_date = True if int(body['is_other_date']) else False
        Cart.objects.filter(pk=kwargs['pk']).update(date_order=date, is_other_date=is_other_date)
        if request.user.is_authenticated:
            order = Order.objects.create(client=request.user, cart=Cart.objects.get(id=kwargs['pk']))
        else:
            order = Order.objects.create(session_key=Cart.objects.get(pk=kwargs['pk']).session_key,
                                         cart=Cart.objects.get(id=kwargs['pk']))
        return HttpResponseRedirect(reverse('order:order_premise', args=[order.id]))
    return render(request, 'cartapp/orderEntity-calendar.html')
