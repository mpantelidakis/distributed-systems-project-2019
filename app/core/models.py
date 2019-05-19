import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

# this is the recommended way for retrieving settings
from django.conf import settings


from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.template.defaultfilters import slugify
import itertools
from django.utils import timezone



def image_file_path(instance, filename):
    """Generate file path for new image"""
    # Returns the last item after the split, the extension in our case
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    # helper function that allows us to reliably join
    # 2 strings together to create a valid path
    return os.path.join('uploads/gallery', filename)


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


class UploadedImage(models.Model):
    """UploadedImage object"""
    gallery = models.ForeignKey(
        'Gallery',
        related_name='images',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='images',
        # when a user is deleted, we also delete all the tags
        # that he/she has created
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(blank=True, upload_to=image_file_path)

    # define the string representation of the model
    def __str__(self):
        return self.name
    
    @property
    def owner(self):
        return self.user


class Gallery(models.Model):
    """Gallery object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    # define the string representation of the model
    def __str__(self):
        return self.name
    
    @property
    def owner(self):
        return self.user


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=50)
    friends = models.ManyToManyField("Profile", blank=True)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    modified_at = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            max_length = Profile._meta.get_field('slug').max_length
            self.slug = orig = slugify(self.user.email)[:max_length]
            self.created_at = timezone.now()

            # since e-mails are unique this does nothing atm
            for x in itertools.count(1):
                if not Profile.objects.filter(slug=self.slug).exists():
                    break
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        self.modified_at = timezone.now()
        super(Profile, self).save(*args, **kwargs)
        return Profile

    def __str__(self):
        return str(self.user.email)
    
    @property
    def owner(self):
        return self.user

    def get_absolute_url(self):
    	return "/friends/{}".format(self.slug)
    

# When a user is created, also create a token and a profile
def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            Token.objects.create(user=instance)
        except:
            pass


        
# class FriendRequest(models.Model):
#     to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user',on_delete=models.CASCADE)
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user',on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True) # set when created 

#     def __str__(self):
#         return "From {}, to {}".format(self.from_user.name, self.to_user.name)

#     @property
#     def owner(self):
#         return self.from_user

class Comment(models.Model):

    image = models.ForeignKey(UploadedImage, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='comment_likes')
    # dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='comment_dislikes')
    comment_text = models.CharField(max_length=1024)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    edited_at = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(Comment, self).save(*args, **kwargs)
        return Comment

    def __str__(self):
        return 'Comment of {} to image {}'.format(self.user, self.image)

    @property
    def owner(self):
        return self.user

    # def get_api_like_url(self):
    #     return reverse('api:comments-like',args=[self.id])

    # def get_api_dislike_url(self):
    #     return reverse('api:comments-dislike',args=[self.id])