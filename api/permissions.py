from rest_framework import permissions
from .models import Groups, GroupTasks

class IsGroupAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only group admins to update or delete tasks.
    """
    def has_permission(self, request, view):
        # Allow read-only actions for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow updates or deletes if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Get the group from the URL
        group_id = view.kwargs['group_pk']
        group = Groups.objects.get(id=group_id)

        # Check if the user is an admin of the group
        return group.is_admin(request.user)

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is an admin of the group the task belongs to.
        """
        # Allow read-only actions for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the task belongs to a group and if the user is an admin of that group
        group = obj.group  # Group of the task (obj is the GroupTasks instance)
        return group.is_admin(request.user)
