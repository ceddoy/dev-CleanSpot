from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView

from orderapp.forms import AddPremiseToOrderForm
from orderapp.models import Order


class AddPremiseToOrderView(FormView):
    form_class = AddPremiseToOrderForm
    success_url = '/'
    template_name = 'orderapp/orderEntity-rooms.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            premise_order = form.save()
            if request.user.is_authenticated:
                Order.objects.filter(pk=kwargs['pk']).update(premise=premise_order)
            else:
                Order.objects.filter(session_key=Order.objects.get(pk=kwargs['pk']).session_key).update(
                    premise=premise_order)
                request.session['order_id'] = kwargs['pk']
                print(request.session.__dict__)
                request.session.modified = True
                # тут какое-нибудь сообщение, о том что надо анониму авторизироваться для дальшей работы
                # и после перенаправляет на авторизацию
                return HttpResponseRedirect(reverse('auth:login'))

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
