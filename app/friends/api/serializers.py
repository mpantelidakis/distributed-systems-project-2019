from rest_framework.serializers import ModelSerializer

from core.models import Profile

class ProfileListSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'slug', 'friends',)
        read_only_fields = ('id', 'user',)

class ProfileDetailSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'slug', 'friends',)
        read_only_fields = ('id', 'user',)