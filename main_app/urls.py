from django.urls import path
from .views import Home , Tickets
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('tickets/', Tickets.as_view(), name='ticket-index'),

]