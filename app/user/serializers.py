"""
Serializers for user API view.
"""

from django.contrib.auth import (get_user_model, authenticate)
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for user API"""
    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {
            'password':{'write_only':True, 'min_length':5}
        }

    def create(self, validated_data):
        """ Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    '''Serializer for user auth token'''

    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type':'password'},
        trim_whitespace = False,
    )