from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import UploadedImage, Gallery
from gallery.serializers import UploadedImageSerializer, GallerySerializer
from PIL import Image
import tempfile
import os

IMAGES_URL = reverse('gallery:uploadedimage-list')
GALLERIES_URL = reverse('gallery:gallery-list')


def image_upload_url():
    """Return URL for image upload"""
    return reverse('gallery:uploadedimage-list')


def sample_gallery(user, title='NiceG'):
    """Create and return a sample gallery"""
    return Gallery.objects.create(user=user, title=title)


def sample_uploaded_img(user, gallery, name='ImageSample'):
    """Create and return an UploadedImage"""
    return UploadedImage.objects.create(user=user, gallery=gallery, name=name)


class PublicImagesApiTests(TestCase):
    """Test the publicly available images API"""

    def SetUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(IMAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class ImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.gallery = sample_gallery(user=self.user)
        self.uploaded_img = sample_uploaded_img(
                user=self.user, gallery=self.gallery
            )

    # function that runs after the test is finished
    def tearDown(self):
        self.uploaded_img.image.delete()

    def test_upload_image_to_gallery(self):
        """Test uploading an image to gallery"""
        url = image_upload_url()
        res = self.client.get(GALLERIES_URL)

        galleries = Gallery.objects.all().order_by('-title')
        serializer = GallerySerializer(galleries, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        # it creates a named temporary file on the system
        # at a random location usually /tempfolder
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            # black square 10x10
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')

            # set the pointer back to the beginning of the file
            ntf.seek(0)

            # to tell django that we need to make a multipart form request
            # a form that consists of data instead of a json object
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.uploaded_img.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.sample_uploaded_img.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url()
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_filter_reciped_by_tags(self):
    #     """Test returning recipes with specific tags"""
    #     recipe1 = sample_recipe(user=self.user, title='Thai vegetable curry')
    #     recipe2 = sample_recipe(user=self.user, title='Aubergine with tahini')
    #     tag1 = sample_tag(user=self.user, name='Vegan')
    #     tag2 = sample_tag(user=self.user, name='Vegetarian')
    #     recipe1.tags.add(tag1)
    #     recipe2.tags.add(tag2)
    #     recipe3 = sample_recipe(user=self.user, title='Fish and chips')

    #     # return only recipes with tag1 or tag2
    #     res = self.client.get(
    #         RECIPES_URL,
    #         {'tags': f'{tag1.id},{tag2.id}'}
    #     )

    #     serializer1 = RecipeSerializer(recipe1)
    #     serializer2 = RecipeSerializer(recipe2)
    #     serializer3 = RecipeSerializer(recipe3)

    #     self.assertIn(serializer1.data, res.data)
    #     self.assertIn(serializer2.data, res.data)
    #     self.assertNotIn(serializer3.data, res.data)

    # def test_filter_recipes_by_ingredients(self):
    #     """Test returning recipes with specific ingredients"""
    #     recipe1 = sample_recipe(user=self.user, title='Posh beans on toast')
    #     recipe2 = sample_recipe(user=self.user, title='Chicken cacciatore')
    #     ingredient1 = sample_ingredient(user=self.user, name='Feta cheese')
    #     ingredient2 = sample_ingredient(user=self.user, name='Chicken')
    #     recipe1.ingredients.add(ingredient1)
    #     recipe2.ingredients.add(ingredient2)
    #     recipe3 = sample_recipe(user=self.user, title='Steak and mushrooms')

    #     # return only recipes with tag1 or tag2
    #     res = self.client.get(
    #         RECIPES_URL,
    #         {'ingredients': f'{ingredient1.id},{ingredient2.id}'}
    #     )

    #     serializer1 = RecipeSerializer(recipe1)
    #     serializer2 = RecipeSerializer(recipe2)
    #     serializer3 = RecipeSerializer(recipe3)

    #     self.assertIn(serializer1.data, res.data)
    #     self.assertIn(serializer2.data, res.data)
    #     self.assertNotIn(serializer3.data, res.data)

# class PrivateIngredientsApiTests(TestCase):
#     """Test the private ingredients API"""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             'test@gmail.com',
#             'testpass'
#         )
#         self.client.force_authenticate(self.user)

#     def test_retrieve_ingredient_list(self):
#         """Test retrieving a list of ingredients"""
#         Ingredient.objects.create(user=self.user, name='Kale')
#         Ingredient.objects.create(user=self.user, name='Salt')

#         res = self.client.get(INGREDIENTS_URL)

#         ingredients = Ingredient.objects.all().order_by('-name')
#         serializer = IngredientSerializer(ingredients, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)

#     def test_ingredients_limited_to_user(self):
#         """Test that ingredients for the authenticated user are returned"""
#         user2 = get_user_model().objects.create_user(
#             'other@gmail.com',
#             'testpass'
#         )
#         Ingredient.objects.create(user=user2, name='Vinegar')

#         ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

#         res = self.client.get(INGREDIENTS_URL)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(res.data), 1)
#         self.assertEqual(res.data[0]['name'], ingredient.name)

#     def test_create_ingredient_successful(self):
#         """Test that a new ingredient is created"""
#         payload = {'name': 'Cabbage'}
#         self.client.post(INGREDIENTS_URL, payload)
#         exists = Ingredient.objects.filter(
#             user=self.user,
#             name=payload['name'],
#         ).exists()
#         self.assertTrue(exists)

#     def test_create_ingredient_invalid(self):
#         """Test creating invalid ingredient fails"""
#         payload = {'name': ''}
#         res = self.client.post(INGREDIENTS_URL, payload)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_retrieve_ingredients_assigned_to_recipes(self):
#         """Test filtering ingredients by those assigned to recipes"""
#         ingredient1 = Ingredient.objects.create(
#             user=self.user, name='Apples'
#         )
#         ingredient2 = Ingredient.objects.create(
#             user=self.user, name='Turkey'
#         )
#         recipe = Recipe.objects.create(
#             title='Apple crumble',
#             time_minutes=5,
#             price=10.00,
#             user=self.user
#         )
#         recipe.ingredients.add(ingredient1)

#         res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

#         serializer1 = IngredientSerializer(ingredient1)
#         serializer2 = IngredientSerializer(ingredient2)

#         self.assertIn(serializer1.data, res.data)
#         self.assertNotIn(serializer2.data, res.data)

#     def test_retrieve_ingredients_assigned_unique(self):
#         """Test filtering ingredients by assigned returns unique items"""
#         ingredient = Ingredient.objects.create(user=self.user, name='Eggs')
#         Ingredient.objects.create(user=self.user, name='Cheese')
#         Recipe.objects.create(
#             title='Eggs benedict',
#             time_minutes=30,
#             price=12.00,
#             user=self.user
#         )
#         recipe2 = Recipe.objects.create(
#             title='Coriander eggs on toast',
#             time_minutes=20,
#             price=5.00,
#             user=self.user
#         )
#         recipe2.ingredients.add(ingredient)

#         res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

#         self.assertEqual(len(res.data), 1)
