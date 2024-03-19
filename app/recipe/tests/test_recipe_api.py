"""
    Test for recipe APIs.
"""

from decimal import Decimal

from core.models import Recipe
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient


def create_recipe(user, **params):
    '''Create and return the recipes'''
    default = {
        'title':'sample recipe',
        'description':'example',
        'price' : Decimal('5.50'),
        'link' : 'www.example.com/test.pdf',
        'time_minutes':22
    }
    default.update(params)
    recipe = Recipe.objects.create(user= user, **default)
    return recipe