from django.db import models
from django.contrib.auth.models import User

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
    members = models.ManyToManyField(User, through='Membership', related_name='joinedgroups')

    #ensure that no group under the same company name share the same group name
    class Meta:
        unique_together = ('company_name', 'group_name')

    def __str__(self):
        return f'{self.company_name} has {self.group_name}'
    
    def add_admin(self, user):
        """assign the user as an admin of the group"""
        Membership.objects.create(user=user, group=self, role__iexact='admin')
    
    def is_admin(self,user):
        """check if a user is an admin of a group"""
        return Membership.objects.filter(user=user, role__ixact='admin').exists()
    
    def assign_task(self, user, target_user, task_title, task_description=None, priority='medium', deadline=None):
        """assign a task to a member in a group"""
        if not  self.is_admin(user):
            raise PermissionError("only admins can add new members jr")
        
        if not Membership.objects.filter(user=target_user, group=self).exists():
            raise PermissionError("only group members can get task assignments kr")
        
        GroupTasks.objects.create(
            group=self, 
            task_title=task_title, 
            task_description=task_description, 
            assigned_to=target_user, 
            task_priority=priority, 
            deadline=deadline
            )
           

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
    


#if my application requires highly specific role-based logic that is difficult to represent
#with django's build in permissions(eg, tracking join requests, per-group custom roles like 'group admin'),
#a custom model is more appropriate

#adding a membership  model for role management
class Membership(models.Model):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('member', 'member'),
    )
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name = 'membership')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='membership')
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='member')
    join_request = models.BooleanField(default=False) #tracks if the user has requested to join the group

    class Meta:
        unique_together = ('user', 'group') #prevent duplicate membership(a user does not appear more than once in a particular group)

    def __str__(self):
        return f"{self.user.username} in {self.group.group_name} as {self.role}"
    
    def approve_join_requests(self, join_request):
        """approve a users request to join a group"""
        if not isinstance(join_request, JoinRequest):
            raise ValueError("Invalid join request")
        
        Membership.objects.create(
            user=join_request.user,
            group=join_request.group,
            role='member'
        )
        join_request.is_approved= True
        join_request.save()
       
    def deny_join_request(self, join_request):
        """deny a users request to join a group"""
        if not isinstance(join_request, JoinRequest):
            raise ValueError("invalid join request presented")
        join_request.delete()


class JoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_request')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='join_request')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #prevent duplicate join requests
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.username} requested to join {self.group.group_name}"
