from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import User

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer

class UserProfileView(generics.RetrieveAPIView):
    """
    Authenticated users can GET (view) and PUT/PATCH (update) their own profile.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
