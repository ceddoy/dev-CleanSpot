from django.urls import path

from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('main_order/<slug:usertypeforservicetype_slug>/<slug:servisetype_slug>/',
         mainapp.PrivateSupportingTemplateView.as_view(), name='main_order'),

]
