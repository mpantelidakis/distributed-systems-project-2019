from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@gmail.com', password='testpass'):
    """create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        # should raise a ValueError when successful
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_image_str(self):
        """Test the image string representation"""
        user = sample_user()
        gallery = models.Gallery.objects.create(
            user=user,
            name='Summer'
        )
        image = models.UploadedImage.objects.create(
            user=user,
            gallery=gallery,
            name='niceImage'
        )
        self.assertEqual(str(image), image.name)

    def test_gallery_str(self):
        """Test the gallery string representation"""
        gallery = models.Gallery.objects.create(
            user=sample_user(),
            name='Summer'
        )
        self.assertEqual(str(gallery), gallery.name)

    # uuid4 is a function inside the uuid module
    # that generates a unique uuid version 4
    @patch('uuid.uuid4')
    def test_recipe_filename_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        # recipe_image_file_paths accepts 2 parameters
        # first one is the instance which is required
        # by django for the upload_to argument
        # second one is the file name of the original file that
        # is added.
        # The reason we pass the second param is that we want to keep
        # the file extension as it is but we are going to replace the
        # first part 'myimage' with the uuid
        file_path = models.image_file_path(None, 'myimage.jpg')

        # f string, can have variables
        exp_path = f'uploads/gallery/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
