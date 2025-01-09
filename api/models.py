from django.db import models
from django.contrib.auth.models import User

# class User(AbstractUser):
#     # Adding related_name to groups and user_permissions to avoid conflicts
#     groups = models.ManyToManyField(
#         'auth.Group', 
#         related_name='api_user_set',  # Rename the reverse accessor for groups
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission', 
#         related_name='api_user_permissions',  # Rename the reverse accessor for permissions
#         blank=True
#     )


class UserTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usertasks')
    task_title = models.CharField(max_length=100)
    TASK_TYPE = (
        ('work', 'work'),
        ('personal','personal'),
        ('errands', 'errands'),
    )
    task_category = models.CharField(max_length=20, choices=TASK_TYPE)
    TASK_PRIO = (
        ('high', 'high'),
        ('medium', 'medium'),
        ('low','low')
    )
    task_priority = models.CharField(max_length=20, choices=TASK_PRIO, default='low')
    task_description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task_tile}"


class Groups(models.Model):
    company_name = models.CharField(max_length=100)
    group_name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='joinedgroups')

    #ensure that no group under the same company name share the same group name
    class Meta:
        unique_together = ('company_name', 'group_name')

    def __str__(self):
        return f'{self.company_name} has {self.group_name}'


class GroupTasks(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='grouptasks')
    task_title = models.CharField(max_length=100, null=False)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='usergrouptasks')
    TASK_PRIO = (
        ('high', 'high'),
        ('medium', 'medium'),
        ('low', 'low')
    )
    task_priority = models.CharField(max_length=20, choices=TASK_PRIO, default='high')
    task_description = models.TextField(null=True)
    deadline = models.DateTimeField(null=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.group} has {self.task_title} assigned to {self.assigned_to} "