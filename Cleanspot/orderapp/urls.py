from django.urls import path

import orderapp.views as orderapp

app_name = 'orderapp'

urlpatterns = [
    path('<int:pk>/premise/', orderapp.AddPremiseToOrderView.as_view(), name='order_premise'),
    path('<int:pk>/your_order/', orderapp.YourOrderDetailView.as_view(), name='your_order'),
    path('anonymous_order/', orderapp.AnonymousOrderTemplateView.as_view(), name='anonymous_order'),
]
