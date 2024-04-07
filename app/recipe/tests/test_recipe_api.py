"""
    Test for recipe APIs.
"""

import email
from decimal import Decimal

from core.models import Recipe
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPE_URL = reverse('recipe:recipe-list')

def details_url(recipe_id):
    '''Create and return the recipe details URL'''
    return reverse('recipe:recipe-detail', args=[recipe_id])

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

def create_user(**params):
    '''Create and return the user'''
    return get_user_model().objects.create_user(**params)

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
        self.user = create_user(
            email ='testuser@gmail.com',
            password ='test123'
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
        other_user = create_user(
            email ='test123@gmail.com',
            password = 'pass123'
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serialize = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialize.data)

    def test_get_recipe_details(self):
        '''Test get recipe details'''

        recipe = create_recipe(user=self.user)
        url = details_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        '''Test creating recipe'''

        payload = {
            'title':'sample recipe',
            'time_mintes' : 20,
            'price': Decimal('5.99')
        }

        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        '''Test Partial update for the recipe'''
        original_link = 'http://example.com/recipe.pdf'
        recipe = create_recipe(
            user = self.user,
            title = 'sample recipe',
            link = original_link
        )
        payload = {'title' : 'new sample recipe'}
        url = details_url(recipe.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update_recipe(self):
        '''Test full updated recipe'''
        recipe = create_recipe(
            user = self.user,
            title = 'sample recipe',
            link = 'http://test.com/recipe.pdf',
            price = Decimal('5.99')
        )

        payload = {'title': 'updated recipe', 'link': 'http://test.me/recipe_2.pdf', 'price': Decimal('9.99')}

        url = details_url(recipe.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_return_error(self):
        '''Test changing the user results error'''

        new_user = create_user(email = 'naveen@nvn.in', password='naveen0987')
        recipe = create_recipe(self.user)
        payload =  {'user': new_user.id}
        url = details_url(recipe.id)
        self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        '''Test deelete recipe'''
        recipe = create_recipe(user=self.user)
        url = details_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_recipe_other_user_delete_error(self):
        '''Test try to delete other user recipes gives error'''

        new_user = create_user(email = 'naveen@nvn.in', password='naveen0987')
        recipe = create_recipe(user=new_user)
        url = details_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())