"""
view for User APIs.
"""

from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """ Create new user in the app."""
    serializer_class = UserSerializer
