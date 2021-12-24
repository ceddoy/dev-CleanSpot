from django.urls import path

import profileapp.views as profileapp

app_name = 'profileapp'

urlpatterns = [

    path('lk_my_data/', profileapp.edit, name='lk_my_data'),
    path('lk_order_history/', profileapp.lk_order_history, name='lk_order_history'),
    path('lk_current_order/', profileapp.lk_current_order, name='lk_current_order'),
    # path('lk_my_premises/', profileapp.lk_my_premises, name='lk_my_premises'),
    path('lk_my_premises/', profileapp.LkMyPremisesView.as_view(), name='lk_my_premises'),
    path('lk_my_premises/delete/<int:pk>/', profileapp.lk_my_premises_delete, name='lk_my_premises_delete'),
    path('lk_add_order/', profileapp.lk_add_order, name='lk_add_order'),

    path('change_password/', profileapp.change_password, name='change_password'),

    path('lk_admin_cleaner_add/', profileapp.lk_admin_cleaner_add, name='lk_admin_cleaner_add'),
    path('lk_admin_cleaner_list/', profileapp.lk_admin_cleaner_list, name='lk_admin_cleaner_list'),
    path('lk_admin_cleaner_edit/<int:pk>/', profileapp.lk_admin_cleaner_edit, name='lk_admin_cleaner_edit'),
    path('lk_admin_history/', profileapp.lk_admin_history, name='lk_admin_history'),
    path('lk_admin_price/', profileapp.lk_admin_price, name='lk_admin_price'),
    path('lk_admin_del/<int:pk>/', profileapp.lk_admin_del, name='lk_admin_del'),
    path('lk_admin_users_list/', profileapp.lk_admin_users_list, name='lk_admin_users_list'),
    path('lk_admin_users_del/<int:pk>/', profileapp.lk_admin_users_del, name='lk_admin_users_del'),
    path('lk_admin_users_edit/<int:pk>/', profileapp.lk_admin_users_edit, name='lk_admin_users_edit'),

    path('lk_partner_active_request/', profileapp.LkPartnerRequestView.as_view(), name='lk_partner_active_request'),
    path('lk_partner_active_orders/', profileapp.LkPartnerOrdersView.as_view(), name='lk_partner_active_orders'),
    path('lk_partner_history_orders/', profileapp.LkPartnerHistoryOrderView.as_view(), name='lk_partner_history_orders'),
]
