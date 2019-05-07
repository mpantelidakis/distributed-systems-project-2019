from rest_framework.generics import ListAPIView, RetrieveAPIView

from core.models import Profile
from .serializers import ProfileListSerializer, ProfileDetailSerializer

class ProfileListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer

class ProfileDetailAPIView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = 'slug'