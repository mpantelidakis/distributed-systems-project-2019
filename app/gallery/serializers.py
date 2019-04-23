from rest_framework import serializers

from core.models import Tag, UploadedImage, Gallery


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class UploadedImageSerializer(serializers.ModelSerializer):
    """Serializer for image objects"""

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    gallery = serializers.PrimaryKeyRelatedField(
        queryset=Gallery.objects.all()
    )

    # overriding __init__ to filter galleries
    def __init__(self, *args, **kwargs):
        super(UploadedImageSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        self.fields['gallery'].queryset = Gallery.objects.filter(
                                                    user=request_user
                                                )

    class Meta:
        model = UploadedImage
        fields = ('id', 'name', 'tags', 'gallery', 'image')
        read_only_fields = ('id',)


class GallerySerializer(serializers.ModelSerializer):
    """Serializer for gallery objects"""

    class Meta:
        model = Gallery
        fields = ('id', 'title')
        read_only_fields = ('id',)
