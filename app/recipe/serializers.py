'''
Serializers for recipe api
'''



from core.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_mintes', 'price', 'link']
        read_only_fields = ['id']