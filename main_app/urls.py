from django.urls import path
from . import views  

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('tickets/', views.Tickets.as_view(), name='ticket-index'),
    path('tickets/<int:ticket_id>/', views.TicketDetail.as_view(), name='ticket-detail'),
    path('tickets/<int:ticket_id>/worklogs/', views.WorkLogsIndex.as_view(), name='worklog-index'),
    path('tickets/<int:ticket_id>/reactions/', views.ReactionsIndex.as_view(), name='reaction-index'),
    path('users/<int:user_id>/profile/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('users/signup/', views.CreateUserView.as_view(), name='signup'),
    path('users/login/', views.LoginView.as_view(), name='login'),
    path('users/token/refresh/', views.VerifyUserView.as_view(), name='token_refresh'),
]

