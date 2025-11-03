from rest_framework import serializers
from .models import Ticket, WorkLog , Reaction , Profile
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import User 
#-----------------------------------------------------------------------------------------
# Ticket 
class TicketSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta: 
        model = Ticket
        exclude = ['created_at']

#-----------------------------------------------------------------------------------------
#WorkLog
class WorkLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLog
        fields = '__all__'
#-----------------------------------------------------------------------------------------
# Reaction
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'

#-----------------------------------------------------------------------------------------
# Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'profile']

#-----------------------------------------------------------------------------------------
# user 
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user