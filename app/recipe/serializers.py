'''
Serializers for recipe api
'''



from core.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    '''Serializer for Recipes.'''

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_mintes', 'price', 'link', 'tags']
        read_only_fields = ['id']

class RecipeDetailSerializer(RecipeSerializer):
    '''Serializer for recipe detail views.'''

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']