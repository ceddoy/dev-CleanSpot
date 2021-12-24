from django.views.generic import ListView

from common.menu import LK_MAIN_MENU, LK_PARTNER_MENU
from orderapp.models import Order


class LkPartnerRequestView(ListView):
    template_name = 'profileapp/lk_partner_request.html'
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LkPartnerRequestView, self).get_context_data()
        context.update({
            'lk_admin_main_menu': LK_MAIN_MENU,
            'lk_partner_menu': LK_PARTNER_MENU,
        })


class LkPartnerOrdersView(ListView):
    pass


class LkPartnerHistoryOrderView(ListView):
    pass
