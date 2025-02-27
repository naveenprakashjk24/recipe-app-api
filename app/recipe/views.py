'''
View for recipe APIs
'''

from core.models import Recipe, Tag
from recipe import serializers
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RecipeViewSet(viewsets.ModelViewSet):
    '''View manage for recipe APIs'''

    serializer_class = serializers.RecipeDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes =[TokenAuthentication]
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')
        # return self.queryset.all().order_by('-id')

    def get_serializer_class(self):
        '''Return serializer class for request'''
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        '''create recipe'''
        serializer.save(user=self.request.user)

class TagViewSet(mixins.UpdateModelMixin, 
                 mixins.ListModelMixin, viewsets.GenericViewSet):
    '''Manage Tags in the database'''
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Filter queryset to authendicated by user'''
        return self.queryset.filter(user=self.request.user).order_by('-name')