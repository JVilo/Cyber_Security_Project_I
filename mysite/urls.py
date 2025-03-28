from django.contrib import admin
from django.urls import include, path
from vulnerable_app import views  # Ensure the import is correct

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('restricted/', views.restricted_view, name='restricted'),
    path('user-input/', views.user_input_view, name='user_input'),
    path('change-role/<int:user_id>/', views.change_user_role, name='change_role'),  # Correct URL pattern
    path('create_test_users/', views.create_test_users, name='create_test_users'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('trigger_error/', views.trigger_error, name='trigger_error'),
    path('', include('vulnerable_app.urls')),
]