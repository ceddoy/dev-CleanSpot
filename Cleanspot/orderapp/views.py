from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView, DetailView, TemplateView

from mainapp.models import Premises
from orderapp.forms import AddPremiseToOrderForm
from orderapp.models import Order
from profileapp.services import get_user


class AddPremiseToOrderView(FormView):
    form_class = AddPremiseToOrderForm
    success_url = '/'
    template_name = 'orderapp/orderEntity-rooms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['service_type_name'] = self.request.session['servise_type']
        context['days'] = ' '.join(self.request.session['days'])
        context['cleaning_time'] = self.request.session['cleaning_time']
        context['number_stuff'] = self.request.session['number_stuff']
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            premise_order = form.save()
            if request.user.is_authenticated:
                Order.objects.filter(pk=kwargs['pk']).update(premise=premise_order)
                request.session['order_id'] = kwargs['pk']
            else:
                Order.objects.filter(session_key=Order.objects.get(pk=kwargs['pk']).session_key).update(
                    premise=premise_order)
                # сессия, чтобы потом id order добавить к анониму
                request.session['order_id'] = kwargs['pk']
                request.session.modified = True

            # Выводим страницу со сформированным заказом
            return HttpResponseRedirect(reverse('order:your_order', args=[kwargs['pk']]))

            # тут какое-нибудь сообщение, о том что надо анониму авторизироваться для дальшей работы
            # и после перенаправляет на авторизацию
            # return HttpResponseRedirect(reverse('auth:login'))

            # return self.form_valid(form)
        else:
            return self.form_invalid(form)


class YourOrderDetailView(DetailView):
    model = Order
    template_name = 'orderapp/orderEntity-your_order.html'
    context_object_name = 'order'


class AnonymousOrderTemplateView(TemplateView):
    template_name = 'orderapp/orderEntity-anonymous_auth.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated:
            user = get_user(request.user)
            order_id = request.session.get('order_id')
            Premises.objects.filter(pk=Order.objects.get(pk=order_id).premise.pk).update(premises_owner=user)
            del request.session['order_id']
            return HttpResponseRedirect(reverse('profileapp:lk_current_order', args=[user.email]))
        else:
            return self.render_to_response(context)
