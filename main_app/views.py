from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404   
from .models import Ticket
from .serializers import TicketSerializer



class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the MTRIX API home route!'}
        return Response(content)

class Tickets(APIView):
    serializer_class = TicketSerializer

    def get(self, request):
        try:
            tickets = Ticket.objects.all()
            serializer = self.serializer_class(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TicketDetail(APIView):
    serializer_class = TicketSerializer
    lookup_field = 'id'

    def get(self, request, ticket_id):
        try:
            obj = get_object_or_404(Ticket, id=ticket_id)   
            serializer = TicketSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, ticket_id):
        try:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            serializer = self.serializer_class(ticket, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, ticket_id):
        try:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            ticket.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
