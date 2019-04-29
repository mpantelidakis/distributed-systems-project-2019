from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, UploadedImage, Gallery

from gallery import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # overriding the get_queryset function
    # to filter returned objects
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            # this checks if FK image of a tag is null,
            # so it returns only tags
            # that are assigned to images
            queryset = queryset.filter(uploadedimage__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class DisplayImagesViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin):
    """Display images in the database"""
    queryset = UploadedImage.objects.all()
    serializer_class = serializers.ImageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class UploadImageViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin):
    """Upload an image in the database"""
    queryset = UploadedImage.objects.all()
    serializer_class = serializers.UploadNewImageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class GalleryViewSet(viewsets.ModelViewSet):
    """Manage galleries in the database"""
    serializer_class = serializers.GallerySerializer
    queryset = Gallery.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        # filter queryset using tags if provided as an arg in the get request
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset

        if tags:
            tags_ids = self._params_to_ints(tags)
            # tags__id__in : Django synstax for filtering on foreign keys
            # filter by ID on the remote table
            # in: function. Return all the tags which have their ID inside
            # the list tags_ids
            queryset = queryset.filter(tags__id__in=tags_ids)

        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    # function used to retrieve the serializer class for
    # a particular request. Override this function to change
    # the serializer class for different actions that are available
    # in the recipe viewset
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.GalleryDetailSerializer
        elif self.action == 'custom_action':
            return serializers.GalleryCustomSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    # custom action, detail=True makes action available for a specific recipe
    # that has been already created
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def custom_action(self, request, pk=None):
        """Upload an image to a recipe"""
        gallery = self.get_object()
        serializer = self.get_serializer(
            gallery,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
