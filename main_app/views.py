from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Ticket
from .serializers import TicketSerializer

# Define the home view
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the MTRIX API home route!'}
        return Response(content)
        
class Tickets(APIView):
    serializer_class = TicketSerializer

    def get(self, request):
        try:
            queryset = Ticket.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)