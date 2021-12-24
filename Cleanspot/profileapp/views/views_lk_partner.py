from django.views.generic import ListView

from common.menu import LK_MAIN_MENU, LK_PARTNER_MENU
from orderapp.models import Order


class LkPartnerRequestView(ListView):
    template_name = 'profileapp/lk_partner_request.html'
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LkPartnerRequestView, self).get_context_data()
        queryset = Order.objects.filter(status='SC', premise__premises_city=self.request.user.city).\
            order_by('created_at')
        page_size = 4
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context.update({
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'order_list': queryset,
                'lk_admin_main_menu': LK_MAIN_MENU,
                'lk_partner_menu': LK_PARTNER_MENU,
            })
        else:
            context.update({
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'order_list': queryset,
                'lk_admin_main_menu': LK_MAIN_MENU,
                'lk_partner_menu': LK_PARTNER_MENU,
            })
        return context


class LkPartnerOrdersView(ListView):
    template_name = 'profileapp/lk_partner_orders.html'
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LkPartnerOrdersView, self).get_context_data()
        context.update({
            'lk_admin_main_menu': LK_MAIN_MENU,
            'lk_partner_menu': LK_PARTNER_MENU,
        })
        return context


class LkPartnerHistoryOrderView(ListView):
    template_name = 'profileapp/lk_partner_history.html'
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LkPartnerHistoryOrderView, self).get_context_data()
        context.update({
            'lk_admin_main_menu': LK_MAIN_MENU,
            'lk_partner_menu': LK_PARTNER_MENU,
        })
        return context
