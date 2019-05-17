from rest_framework import serializers

from core.models import Profile

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.validators import UniqueTogetherValidator


User = get_user_model()

profile_detail_url = serializers.HyperlinkedIdentityField(
    view_name='friends-api:profile-detail',
    lookup_field='slug'
)

class UserExclusionPrimaryKeyRelatedField(serializers.StringRelatedField):
    """
    Custom primary key related field to exclude the object associated
    with the currently logged in user
    """

    def to_internal_value(self, value):
        request = self.context.get('request', None)
        user = get_object_or_404(User,email=value)
        profile = get_object_or_404(Profile,user=user.id)  
        if profile and profile.user is not request.user:
            return profile
       

class ProfileListSerializer(serializers.ModelSerializer):
    """Serializer for Profile list"""
    url = profile_detail_url
    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = ('id', 'url', 'user', 'slug',)
        read_only_fields = ('id', 'user',)


class ProfileDetailSerializer(serializers.ModelSerializer):
    """Serializer for Retrieving and Updating profiles"""
    friends = UserExclusionPrimaryKeyRelatedField(many=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'slug', 'friends', 'created_at', 'modified_at')
        read_only_fields = ('id', 'user', 'created_at', 'modified_at')

    def validate_friends(self, value):
        """Enforce that a user cannot add himself"""
        user = self.context['request'].user
        user_profile = get_object_or_404(Profile, user=user)

        if user_profile in value:
            raise serializers.ValidationError("You cannot add yourself.")
        return value


# class FriendRequestListSerializer(serializers.ModelSerializer):
#     to_user = serializers.StringRelatedField()
#     from_user = serializers.StringRelatedField()

#     class Meta:
#         model = FriendRequest
#         fields = ('id', 'from_user', 'to_user', 'timestamp')
#         read_only_fields = ('id',)


# class FriendRequestCreateSerializer(serializers.ModelSerializer):

#     from_user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )

#     class Meta:
#         model = FriendRequest
#         fields = ('id', 'to_user', 'from_user')
#         read_only_fields = ('id', 'from_user')
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=FriendRequest.objects.all(),
#                 fields=('from_user', 'to_user'),
#                 message =('You have already sent a friend request to this user')
#             )
#         ]

#     #  exclude authenticated user from to_user queryset
#     def __init__(self, *args, **kwargs):
#         super(FriendRequestCreateSerializer, self).__init__(*args, **kwargs)

#         context = kwargs.get('context', None)
#         if context:
#             request_user = self.context['request'].user
#             self.fields['to_user'].queryset = User.objects.exclude(
#                                                         id=request_user.id
#                                                     )
#         else:
#             print('No context is being passed to the serializer')
    

# class FriendRequestDeleteSerializer(serializers.ModelSerializer):
#     to_user = serializers.StringRelatedField()
#     from_user = serializers.StringRelatedField()

#     class Meta:
#         model = FriendRequest
#         fields = ('id', 'from_user', 'to_user', 'timestamp')
#         read_only_fields = ('id',)