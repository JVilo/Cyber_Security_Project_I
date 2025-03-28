from django.urls import path
from . import views

urlpatterns = [
    path('restricted/', views.restricted_view, name='restricted'),
    path('user-input/', views.user_input_view, name='user_input'),
    path('change-role/<int:user_id>/', views.change_user_role, name='change_role'),
    path('create-users/', views.create_test_users_view, name='create_test_users'),
    path('trigger_error/', views.trigger_error, name='trigger_error'),
    
]