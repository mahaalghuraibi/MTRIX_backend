from rest_framework import serializers
from .models import Ticket, WorkLog , Reaction 

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