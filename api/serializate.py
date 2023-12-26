from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task
from datetime import datetime
from django.utils.timezone import now
from base64 import b64decode



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_title(self, value):
        if value.lower() not in ['title', 'sarlavha']:
            raise serializers.ValidationError("Siz notogri title tanlagansiz.")
        return value
    
    def validate(self, date):
        created_date = datetime.fromisoformat(date['created'])
        if created_date['date'] < now():
            raise serializers.ValidationError("siz noto'g'ri sana tanladingiz")
        return date
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created'] = data['created'].isoformat()
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    sorted_tasks = serializers.SerializerMethodField()

    def get_sorted_tasks(self, obj):
        
        related_objects = obj.tasks.all().order_by('-completed')

        serializer = TaskSerializer(related_objects, many=True)
        return serializer.data
    
        
