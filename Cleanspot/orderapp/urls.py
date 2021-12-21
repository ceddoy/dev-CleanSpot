from django.urls import path

import orderapp.views as orderapp

app_name = 'orderapp'

urlpatterns = [
    path('<int:pk>/premise/', orderapp.AddPremiseToOrderView.as_view(), name='order_premise'),
]
