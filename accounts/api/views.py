from rest_framework import generics, permissions
from accounts.models import User
from .serializers import UserProfileSerializer


class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
