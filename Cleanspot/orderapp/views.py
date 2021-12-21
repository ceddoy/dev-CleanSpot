from django.views.generic import FormView

from orderapp.forms import AddPremiseToOrderForm
from orderapp.models import Order


class AddPremiseToOrderView(FormView):
    form_class = AddPremiseToOrderForm
    success_url = '/'
    template_name = 'orderapp/orderEntity-rooms.html'

    # def get_success_url(self):
    #     if self.request.user.is_authenticated:
    #         return str(self.success_url)
    #     else:

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            premise_order = form.save()
            if request.user.is_authenticated:
                Order.objects.filter(pk=kwargs['pk']).update(premise=premise_order)
            else:
                Order.objects.filter(session_key=Order.objects.get(pk=kwargs['pk']).session_key).update(
                    premise=premise_order)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
