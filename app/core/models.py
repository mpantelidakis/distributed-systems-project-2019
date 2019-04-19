import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

# this is the recommended way for retrieving settings
from django.conf import settings


def recipe_image_file_path(instance, filename):
    """Generate file path for new image"""
    # Returns the last item after the split, the extension in our case
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    # helper function that allows us to reliably join
    # 2 strings together to create a valid path
    return os.path.join('uploads/recipe', filename)


class UserManager(BaseUserManager):
    # function can take extra fields
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')

        # normalize_email comes with UserManager and sets email to lowercase
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)  # required for supporting multiple dbs

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password=password,)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    # instead of referencing the user object directly
    # we are going to use the best practice method of
    # retrieving the AUTH_USER_MODEL setting
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,

        # when a user is deleted, we also delete all the tags
        # that he/she has created
        on_delete=models.CASCADE,
    )

    # define the string representation of the model
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # define the string representation of the model
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # the user can provide a link to the recipe
    # blank=True for optional fields
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    # define the string representation of the model
    def __str__(self):
        return self.title
