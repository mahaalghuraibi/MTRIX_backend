from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from django.shortcuts import get_object_or_404   
from .models import Ticket , WorkLog
from .serializers import TicketSerializer , WorkLogSerializer
from .models import Ticket, Reaction
from .serializers import ReactionSerializer
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer, RegisterUserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

#-----------------------------------------------------------------------------------------
# Home
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the MTRIX API home route!'}
        return Response(content)

#-----------------------------------------------------------------------------------------
# Tickets
class Tickets(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer

    def get(self, request):
        try:
            if hasattr(request.user, 'profile'):
                if request.user.profile.role in ['Admin', 'Technician']:
                    tickets = Ticket.objects.all()
                else:
                    tickets = Ticket.objects.filter(user=request.user)
            else:
                tickets = Ticket.objects.filter(user=request.user)
            serializer = self.serializer_class(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(user_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#-----------------------------------------------------------------------------------------
# TicketDetail
class TicketDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer
    lookup_field = 'id'

    def get(self, request, ticket_id):
        try:
            obj = get_object_or_404(Ticket, id=ticket_id)
            if hasattr(request.user, 'profile') and request.user.profile.role == 'Staff':
                if obj.user != request.user:
                    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            serializer = TicketSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, ticket_id):
        try:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            if hasattr(request.user, 'profile') and request.user.profile.role == 'Staff':
                if ticket.user != request.user:
                    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
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
            if hasattr(request.user, 'profile') and request.user.profile.role == 'Staff':
                if ticket.user != request.user:
                    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            ticket.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#-----------------------------------------------------------------------------------------
# WorkLogs
class WorkLogsIndex(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
# Reactions 
class Reactions(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReactionSerializer

    def get(self, request):  
        try:
            reactions = Reaction.objects.all()
            serializer = self.serializer_class(reactions, many=True)
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
# ReactionsIndex 
class ReactionsIndex(APIView):
    permission_classes = [permissions.IsAuthenticated]
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

#-----------------------------------------------------------------------------------------
# ReactionDetail 
class ReactionDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReactionSerializer
    lookup_field = 'id'

    def get(self, request, reaction_id):  
        try:
            object = get_object_or_404(Reaction, id=reaction_id)
            serializer = ReactionSerializer(object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, reaction_id):  
        try:
            reaction = get_object_or_404(Reaction, id=reaction_id)
            if hasattr(request.user, 'profile') and request.user.profile.role == 'Staff':
                if reaction.ticket.user != request.user:
                    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(reaction, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, reaction_id):  
        try:
            reaction = get_object_or_404(Reaction, id=reaction_id)
            if hasattr(request.user, 'profile') and request.user.profile.role == 'Staff':
                if reaction.ticket.user != request.user:
                    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            reaction.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#-----------------------------------------------------------------------------------------
# Profile
class ProfileDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer  

    def post(self, request, user_id):
        try:
            data = request.data.copy()
            data["user"] = int(user_id)

            user = get_object_or_404(User, id=user_id)


            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                Profile.objects.update_or_create(
                    user=user,
                    defaults=serializer.validated_data
                )

                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#-----------------------------------------------------------------------------------------
class UpdateProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def put(self, request):
        try:
            profile, created = Profile.objects.get_or_create(user=request.user)

            new_role = request.data.get('type')
            if new_role is None:
                return Response({'type': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(profile, data={'role': new_role}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#-----------------------------------------------------------------------------------------
# User Signup 
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer 

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#-----------------------------------------------------------------------------------------
# User 
class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                content = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
                return Response(content, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           

#-----------------------------------------------------------------------------------------
# User Verification / Token Refresh
class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            print("refresh token!!!")

            try:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            except Exception as token_error:
                return Response(
                    {"detail": "Failed to generate token.", "error": str(token_error)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as err:
            return Response(
                {"detail": "Unexpected error occurred.", "error": str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )