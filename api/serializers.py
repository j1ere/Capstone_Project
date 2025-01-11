from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])#ensures password is not exposed in API responses and is strong
    username = serializers.CharField(max_length=100, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        #hash the password before saving the user
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserTasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTasks
        fields = ['user', 'task_title', 'task_category', 'task_priority', 'task_description', 'deadline','is_complete']

    def validate_task_category(self, value):
        """ensure that the task category is one of the allowed tasks"""
        valid_categories = dict(UserTasks.TASK_TYPE).keys()
        if value not in valid_categories:
            raise serializers.ValidationError("invalid task category")
        return value
    
    def validate_task_priority(self, value):
        valid_priorities = dict(UserTasks.TASK_PRIO).keys()
        if value not in valid_priorities:
            raise serializers.ValidationError("invalid task priority")
        return value
    
    def validate_deadline(self, value):
        """ensure deadline is in the future if provided"""
        from django.utils import timezone
        #insure the value  `deadline` is timezone aware
        if timezone.is_naive(value):
            raise serializers.ValidationError("Deadline must include timezone information")
        
        #compare with the current time (timezone-aware)
        if value and value <= timezone.now():
            return serializers.ValidationError("date must be in future")
        return value
    
    def validate(self, data):
        """perform crossfield validation"""
        if data['task_priority'] == 'high' and not data['deadline']:
            raise serializers.ValidationError("high priority tasks MUST have a deadline")
        return data
        
