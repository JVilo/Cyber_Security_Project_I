from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models

class UserProfile(AbstractUser):
    role = models.CharField(max_length=255)
    
    # Adding custom related_name to avoid clashes with default User model
    groups = models.ManyToManyField(
        Group,
        related_name='userprofile_set',  # Custom related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='userprofile_set',  # Custom related_name
        blank=True,
    )


class CustomUser(AbstractUser):
    # Override the groups and user_permissions fields with a custom related_name
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # This changes the reverse accessor to avoid conflict
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # This changes the reverse accessor to avoid conflict
        blank=True
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"
