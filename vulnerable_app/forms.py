from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.models import Group


# User Registration Form with Role Selection
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        help_text="Password must be at least 12 characters long, contain at least one uppercase letter, one number, and one special character."
    )
    class Meta:
        model = User
        fields = ['username', 'password']  # Only username and password fields

    # Customize the username field widget to remove the validation message
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),  # Add a placeholder if needed
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Set the password securely
        if commit:
            user.save()
        return user
    
    # cheks the password and tests if it is god enough.
    #def clean_password(self):
    #    password = self.cleaned_data.get('password')
    #    # Check if password meets the length requirement
    #    if len(password) < 12:
    #        raise forms.ValidationError("Password must be at least 12 characters long.")
    #    
    #    # Check if password contains at least one number
    #    if not any(char.isdigit() for char in password):
    #        raise forms.ValidationError("Password must contain at least one number.")
    #    
    #    # Check if password contains at least one uppercase letter
    #    if not any(char.isupper() for char in password):
    #        raise forms.ValidationError("Password must contain at least one uppercase letter.")
    #    
    #    # Check if password contains at least one special character
    #    if not any(char in "!@#$%^&*()" for char in password):
    #        raise forms.ValidationError("Password must contain at least one special character.")
    #    
    #    return password


# Profile Form for additional user details (bio, birth_date, etc.)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date']