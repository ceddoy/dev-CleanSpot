from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('register/step_1/', authapp.register_step_1, name='register_step_1'),
    path('register/step_2/', authapp.register_step_2, name='register_step_2'),
    path('register/complete/', authapp.AuthTemplateView.as_view(), name='registration_complete'),
    path('register/cleaner/', authapp.register_cleaner, name='register_cleaner'),
    path('register/cleaner/complete/', authapp.RegisterCleanerCompleteTemplateView.as_view(), name='register_cleaner'
                                                                                                   '_complete'),
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('verify/<email>/<activation_key>/', authapp.verify, name='verify'),
    # path('change_password/', authapp.change_password, name='change_password'),
    path('password_reset/', authapp.reset_password, name='reset_password'),
    path('password_done/', authapp.AuthPasswordResetDoneView.as_view(), name='done_password'),
    path('password_confirm/<uidb64>/<token>/', authapp.AuthPasswordResetConfirmView.as_view(), name='confirm_password'),
    path('password_complete/', authapp.AuthPasswordResetCompleteView.as_view(), name='complete_password'),
]
