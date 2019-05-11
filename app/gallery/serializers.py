from rest_framework import serializers

from core.models import Tag, UploadedImage, Gallery


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

    
    def validate_name(self, value):
        qs = Tag.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("This tag already exists")
        return value


class GalleryFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Custom primary key related field to filter galleries for the
    logged in user
    """
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(GalleryFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(user=request.user)

class ImageSerializer(serializers.ModelSerializer):
    """Serializer for image objects"""

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    
    gallery = GalleryFilteredPrimaryKeyRelatedField(
        queryset=Gallery.objects.all()
    )

    class Meta:
        model = UploadedImage
        fields = ('id', 'name', 'tags', 'gallery', 'image')
        read_only_fields = ('id',)

    # image names should be unique. why? because!
    def validate_name(self, value):
        user = self.context['request'].user
        qs = UploadedImage.objects.filter(name__iexact=value, user=user)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("This image already exists")
        return value
    
    
class GallerySerializer(serializers.ModelSerializer):
    """Serializer for gallery objects"""

    number_of_images = serializers.SerializerMethodField()
    
    class Meta:
        model = Gallery
        fields = ('id', 'name','number_of_images')
        read_only_fields = ('id','number_of_images')

    def validate_name(self, value):
        user = self.context['request'].user
        qs = Gallery.objects.filter(name__iexact=value, user=user)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("This gallery already exists")
        return value
    
    def get_number_of_images(self, obj):
        """Get the number of images uploaded to the gallery"""
        return obj.images.count()


class GalleryDetailSerializer(serializers.ModelSerializer):
    """Serializer for gallery objects"""

    images = ImageSerializer(many=True)
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Gallery
        fields = ('id', 'owner', 'name', 'images')
        read_only_fields = ('id', 'images')


class ImageDetailSerializer(serializers.ModelSerializer):
    """Serialize an image detail"""
    tags = TagSerializer(many=True)
    gallery = serializers.PrimaryKeyRelatedField(
        queryset=Gallery.objects.all()
    )

    class Meta:
        model = UploadedImage
        fields = ('id', 'name', 'gallery', 'tags', 'image',)
        read_only_fields = ('id', 'image',)

# below serializer won't have image field inside so that the
# user cannot update the image field.
# Mentality is, if u want to modify the image field of an image,
# Go ahead and delete it and then upload a new one.
class ImageDetailSerializerNoImageField(serializers.ModelSerializer):
    """Serializer for PUT/PATCH methods"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    gallery = serializers.PrimaryKeyRelatedField(
        queryset=Gallery.objects.all()
    )

    class Meta:
        model = UploadedImage
        fields = ('id', 'name', 'gallery', 'tags')
        read_only_fields = ('id',)