from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404   
from .models import Ticket , WorkLog
from .serializers import TicketSerializer , WorkLogSerializer
from .models import Ticket, Reaction
from .serializers import ReactionSerializer


#-----------------------------------------------------------------------------------------

class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the MTRIX API home route!'}
        return Response(content)

#-----------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------------------

class WorkLogsIndex(APIView):
    serializer_class = WorkLogSerializer

    def get(self, request, ticket_id):
        try:
            queryset = WorkLog.objects.filter(ticket=ticket_id)
            data = self.serializer_class(queryset, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, ticket_id):
        try:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            data = request.data.copy()
            data["ticket"] = ticket.id

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()

                queryset = WorkLog.objects.filter(ticket=ticket_id)
                worklogs = self.serializer_class(queryset, many=True).data
                return Response(worklogs, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#-----------------------------------------------------------------------------------------

class ReactionsIndex(APIView):
    serializer_class = ReactionSerializer

    def get(self, request, ticket_id):
        try:
            reactions = Reaction.objects.filter(ticket=ticket_id)
            serializer = self.serializer_class(reactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, ticket_id):
        try:
            data = request.data.copy()
            data["ticket"] = ticket_id  
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                reactions = Reaction.objects.filter(ticket=ticket_id)
                return Response(self.serializer_class(reactions, many=True).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)