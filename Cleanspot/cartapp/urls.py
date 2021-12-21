from django.urls import path
from django.views.generic import RedirectView

import cartapp.views as cartapp

app_name = 'cartapp'

urlpatterns = [
    path('', RedirectView.as_view(url='legal_person/general/'), name='cart_main'),
    path('<slug:usertypeforservicetype_slug>/', cartapp.ShowListServicesView.as_view(), name='usertype_services'),
    path('<slug:usertypeforservicetype_slug>/<slug:servisetype_slug>/', cartapp.ShowListServicesView.as_view(),
         name='servicetype_services'),
    path('<slug:usertypeforservicetype_slug>/<slug:servisetype_slug>/<int:pk>/date/',
         cartapp.add_date_to_cart, name='date_for_cart'),
    path('calendar/<int:year>/<int:month>/', cartapp.CalendarTableFormView.as_view(), name='calendar')
]
