from django.urls import path
from . import views

urlpatterns = [
    path('restricted/', views.restricted_view, name='restricted'),
    path('change-role/<int:user_id>/', views.change_user_role, name='change_role'),
    path('create-users/', views.create_test_users_view, name='create_test_users'),
    path('trigger_error/', views.trigger_error, name='trigger_error'),
    path('messages/new/', views.message_form_view, name='message_form'),
    path('messages/', views.show_messages, name='show_messages'),
    path('leak/', views.leak_all_messages, name='leak_all'),
    
]