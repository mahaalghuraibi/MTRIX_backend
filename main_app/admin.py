from django.contrib import admin
from .models import Ticket , WorkLog , Reaction 

admin.site.register(Ticket) # Ticket
#-----------------------------------------------------------------------------------------
admin.site.register(WorkLog) # WorkLog
#-----------------------------------------------------------------------------------------
admin.site.register(Reaction) # Reaction
