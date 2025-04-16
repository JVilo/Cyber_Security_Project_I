from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.html import escape
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm


def trigger_error(request):
    raise Exception("This is a test error triggered by a button click!")
# Uncaught Server Error Endpoint
# def trigger_error(request):
#     if not request.user.is_superuser:
#         return HttpResponse("Not allowed", status=403)
#     raise Exception("Simulated error.")

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to home or any page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to home after logout

@login_required
def restricted_view(request):
    return HttpResponse("This is a restricted view.")

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        # Check if form is valid and then save
        if form.is_valid():
            form.save()  # Save the user (with hashed password)
            return redirect('login')  # Redirect to login page after successful registration
        else:
            # If form is invalid, show an error message
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def create_test_users():
    # Create groups (roles)
    admin_group, created = Group.objects.get_or_create(name='Admin')
    user_group, created = Group.objects.get_or_create(name='User')

    # Create example users
    user1 = User.objects.create_user(username='user1', password='password123')
    user2 = User.objects.create_user(username='user2', password='password123')

    # Assign groups (roles) to users
    user1.groups.add(user_group)
    user2.groups.add(user_group)

    # Create an admin user
    admin_user = User.objects.create_superuser(username='admin', password='admin123')
    admin_user.groups.add(admin_group)

    return HttpResponse("Test users created successfully!")

# You can call this function somewhere in your views.py to ensure test users are created when the server starts
#create_test_users()

def create_test_users_view(request):
    create_test_users()  # Create users and roles on view access
    return HttpResponse("Test users and roles have been created.")

def change_user_role(request, user_id):
    # Ensure the user exists
    user = get_object_or_404(User, id=user_id)
    new_role = request.POST.get("role", "")  # Assume you're sending a POST request to update the role
    
    if new_role:
        user.profile.role = new_role
        user.profile.save()
        return HttpResponse(f"Role updated for user {user.username}.")
    else:
        return HttpResponse("No role provided.", status=400)

def home(request):
    if request.user.is_authenticated:
        # If user is logged in
        username = request.user.username
        return render(request, 'index.html', {'username': username})
    else:
        # If no user is logged in
        return render(request, 'index.html', {'username': None})

# 1. Broken Access Control - No authentication check (vulnerable version)
def restricted_view(request):
    # Vulnerability: Anyone can access this view
    return HttpResponse("This is a restricted view.")

# 1. Broken Access Control - Authentication check (fixed version)
# @login_required
# def restricted_view(request):
#     # Fix: Restrict access to authenticated users
#     return HttpResponse("This is a restricted view.")

# 2. Injection (XSS) - Vulnerable version
def user_input_view(request):
    user_input = request.GET.get("input", "")
    return HttpResponse(f"User input: {user_input}")  # Vulnerable to XSS

# 2. Injection (XSS) - Fixed version
# def user_input_view(request):
#     user_input = request.GET.get("input", "")
#     safe_input = escape(user_input)  # Fix: Escape user input to prevent XSS
#     return HttpResponse(f"User input: {safe_input}")


# 4. Identification and Authentication Failures - Weak password policy (vulnerable version)
# In settings.py, weak password validators are present by default. Let's add a vulnerable view that can change user roles.
# 5. Insecure Design (Broken Access Control on Role Changing)
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def change_user_role(request, user_id):
    # Ensure the user exists
    user = get_object_or_404(User, id=user_id)
    
    # Get new role from POST request (assuming role is a group name)
    new_role = request.POST.get("role", "")
    
    if new_role:
        # Assuming roles are managed using Django's Group model
        group, created = Group.objects.get_or_create(name=new_role)
        user.groups.clear()  # Clear current roles
        user.groups.add(group)  # Assign new role
        
        return HttpResponse(f"Role of {user.username} updated to {new_role}.")
    else:
        return HttpResponse("No role provided.", status=400)

# 4. Identification and Authentication Failures - Strong password policy and role-based access control (fixed version)
# @user_passes_test(is_admin)
# def change_user_role(request, user_id):
#     # Fix: Only users with specific permission can change roles
#     if not request.user.has_perm('webapp.change_user_role'):  # Ensure the user has permission
#         return HttpResponse("Unauthorized", status=403)
#     user = User.objects.get(id=user_id)
#     user.role = request.POST.get("role")
#     user.save()
#     return HttpResponse("Role updated.")