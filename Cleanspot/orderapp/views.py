from django.views.generic import FormView

from profileapp.forms import CleanspotUserAddOrEditPremise


class AddPremiseToOrderView(FormView):
    form_class = CleanspotUserAddOrEditPremise
    success_url = '/'
    template_name = 'orderapp/orderEntity-rooms.html'


