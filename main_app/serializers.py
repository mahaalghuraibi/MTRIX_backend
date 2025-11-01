from rest_framework import serializers
from .models import Ticket, WorkLog , Reaction , Profile
from django.contrib.auth import get_user_model ######

#-----------------------------------------------------------------------------------------
# Ticket 
class TicketSerializer(serializers.ModelSerializer):
    class Meta: #cy
        model = Ticket
        #fields = '__all__'
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