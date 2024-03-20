'''
View for recipe APIs
'''

from core.models import Recipe
from recipe.serializers import RecipeSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RecipeViewSet(viewsets.ModelViewSet):
    '''View manage for recipe APIs'''

    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes =[TokenAuthentication]
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')