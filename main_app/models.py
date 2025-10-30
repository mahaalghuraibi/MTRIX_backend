from django.db import models

# Create your models here.
from django.db import models

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=20)
    #created_by = models.CharField(max_length=100) #ForeignKey relating to user
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title
