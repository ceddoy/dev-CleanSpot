from django.contrib.auth import views
from django.urls import path
from django.views.generic import TemplateView

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('register/<int:pk>', authapp.register, name='register'),
    path('register/complete/', TemplateView.as_view(
        template_name='authapp/register_complete.html'),
        name='registration_complete'),
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('verify/<email>/<activation_key>/', authapp.verify, name='verify'),
    # path('change_password/', authapp.change_password, name='change_password'),
    path('password_reset/', authapp.reset_password, name='reset_password'),
    path('password_done/', views.PasswordResetDoneView.as_view(
        template_name='authapp/password_reset_done.html'),
         name='done_password'),
    path('password_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
        template_name='authapp/password_reset_confirm.html', success_url='/auth/password_complete/'),
         name='confirm_password'),
    path('password_complete/', views.PasswordResetCompleteView.as_view(
        template_name='authapp/password_reset_complete.html'),
         name='complete_password'),

]
