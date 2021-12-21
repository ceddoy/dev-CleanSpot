from django.views.generic import FormView

from orderapp.forms import AddPremiseToOrderForm


class AddPremiseToOrderView(FormView):
    form_class = AddPremiseToOrderForm
    success_url = '/'
    template_name = 'orderapp/orderEntity-rooms.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            print(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
