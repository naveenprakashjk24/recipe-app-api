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

RECIPE_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    '''Create and return the recipes'''
    default = {
        'title':'sample recipe',
        'description':'example',
        'price' : Decimal('5.50'),
        'link' : 'www.example.com/test.pdf',
        'time_mintes':22
    }
    default.update(params)
    recipe = Recipe.objects.create(user=user, **default)
    return recipe


class PublicRecipeAPITest(TestCase):
    '''Test unauthdicated API requests'''

    def setUp(self):
        self.client = APIClient()

    def test_auth_requried(self):
        '''Test auth is required for API calls.'''
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITest(TestCase):
    '''Test authendication for API calls.'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testuser@gmail.com',
            'test123'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipe(self):
        '''Test retriving the recipe lists.'''

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serialize = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialize.data)

    def test_retrive_recipe_list_limited_to_user(self):
        '''Test limted data for users.'''
        other_user = get_user_model().objects.create_user(
            'test123@gmail.com',
            'pass123'
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serialize = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialize.data)