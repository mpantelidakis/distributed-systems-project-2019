from rest_framework import serializers

from core.models import Comment, UploadedImage


class ImageFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Custom primary key related field to filter galleries for the
    logged in user
    """
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(ImageFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        
        # first we get the user's own images
        own_images_queryset =  queryset.filter(user=request.user)
        #print(own_images_queryset)
        
        #then we get the images of all his friends and combine the querries
        user_friends = request.user.profile.friends.all()
        for friend in user_friends:
            images = friend.user.images.all()

            # union
            own_images_queryset |= images

            # print(own_images_queryset)
        return own_images_queryset

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment objects"""

    image = ImageFilteredPrimaryKeyRelatedField(
        queryset=UploadedImage.objects.all()
    )

    class Meta:
        model = Comment
        fields = ('id', 'user', 'image', 'comment_text', 'created_at', 'edited_at')
        read_only_fields = ('id', 'user', 'created_at', 'edited_at')

# class CommentDetailSerializer(serializers.ModelSerializer):
#     """Serializer for comment objects"""

#     class Meta:
#         model = Comment
#         fields = ('id', 'user', 'comment_text', 'created_at')
#         read_only_fields = ('id', 'user', 'created_at',)


class CommentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for comment objects"""

    class Meta:
        model = Comment
        fields = ('id', 'user', 'comment_text', 'created_at')
        read_only_fields = ('id', 'user', 'created_at',)
