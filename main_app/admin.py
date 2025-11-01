from django.contrib import admin
from .models import Ticket , WorkLog , Reaction , Profile  

admin.site.register(Ticket) # Ticket
#-----------------------------------------------------------------------------------------
admin.site.register(WorkLog) # WorkLog
#-----------------------------------------------------------------------------------------
admin.site.register(Reaction) # Reaction
#-----------------------------------------------------------------------------------------
admin.site.register(Profile) #Profile