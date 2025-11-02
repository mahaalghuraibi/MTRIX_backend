from django.db import models
from django.conf import settings ######
from django.contrib.auth.models import User

#-----------------------------------------------------------------------------------------

 # Ticket 
class Ticket(models.Model): # cy
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #
    #created_by = models.CharField(max_length=100) #ForeignKey relating to user
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

#-----------------------------------------------------------------------------------------

# WorkLog
class WorkLog(models.Model):
    TYPE_CHOICES = (
        ('F', 'Fix'),
        ('C', 'Check'),
        ('R', 'Replace'),
    )

    date = models.DateField('Work date')
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='F')  
    note = models.TextField(max_length=500, blank=True, default="")          
    technician_id = models.IntegerField(blank=True, null=True)              
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='worklogs')

    class Meta:
        ordering = ['-date']


#-----------------------------------------------------------------------------------------

# Reaction 
class Reaction(models.Model):
    SCORE_CHOICES = (
        (1, '😐'),
        (2, '🙂'),
        (3, '🤩'),
    )

    ticket   = models.ForeignKey('Ticket', related_name='reactions', on_delete=models.CASCADE)
    staff_id = models.IntegerField() 
    score    = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"T{self.ticket_id} • S{self.staff_id} • {self.score}"


#-----------------------------------------------------------------------------------------

#Profile 
class Profile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Technician', 'Technician'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Staff')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username} ({self.role})"