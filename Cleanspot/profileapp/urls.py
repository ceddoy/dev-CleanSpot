from django.urls import path

import profileapp.views as profileapp

app_name = 'profileapp'

urlpatterns = [

    path('', profileapp.edit, name='edit'),
    path('change_password/', profileapp.change_password, name='change_password'),
    path('lk_admin_cleaner_add/', profileapp.lk_admin_cleaner_add, name='lk_admin_cleaner_add'),
    path('lk_admin_cleaner_list/', profileapp.lk_admin_cleaner_list, name='lk_admin_cleaner_list'),
    path('lk_admin_cleaner_edit/<int:pk>/', profileapp.lk_admin_cleaner_edit, name='lk_admin_cleaner_edit'),
    path('lk_admin_history/', profileapp.lk_admin_history, name='lk_admin_history'),
    path('lk_admin_del/<int:pk>/', profileapp.lk_admin_del, name='lk_admin_del'),
    path('lk_admin_users_list/', profileapp.lk_admin_users_list, name='lk_admin_users_list'),
    path('lk_admin_users_del/<int:pk>/', profileapp.lk_admin_users_del, name='lk_admin_users_del'),
    path('lk_admin_users_edit/<int:pk>/', profileapp.lk_admin_users_edit, name='lk_admin_users_edit'),


]
