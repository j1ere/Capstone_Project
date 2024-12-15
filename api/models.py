from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Adding related_name to groups and user_permissions to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='api_user_set',  # Rename the reverse accessor for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='api_user_permissions',  # Rename the reverse accessor for permissions
        blank=True
    )
# Task model
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
