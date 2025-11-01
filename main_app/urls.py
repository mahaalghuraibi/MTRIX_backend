from django.urls import path
from .views import Home, Tickets , TicketDetail , WorkLogsIndex , ReactionsIndex , ProfileDetail

#-----------------------------------------------------------------------------------------
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('tickets/', Tickets.as_view(), name='ticket-index'),
    path('tickets/<int:ticket_id>/', TicketDetail.as_view(), name='ticket-detail'),
    path('tickets/<int:ticket_id>/worklogs/', WorkLogsIndex.as_view(), name='worklog-index'),
    path('tickets/<int:ticket_id>/reactions/', ReactionsIndex.as_view(), name='reaction-index'),
    path('users/<int:user_id>/profile/', ProfileDetail.as_view(), name='profile-detail'),

]
