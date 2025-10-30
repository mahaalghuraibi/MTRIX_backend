from django.urls import path
from .views import Home, Tickets , TicketDetail   

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('tickets/', Tickets.as_view(), name='ticket-index'),
    path('tickets/<int:ticket_id>/', TicketDetail.as_view(), name='ticket-detail'),
]
