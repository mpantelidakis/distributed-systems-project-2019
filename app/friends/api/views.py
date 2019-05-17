from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)

from core.models import Profile
from rest_framework import status

from .serializers import (
    ProfileListSerializer,
    ProfileDetailSerializer,
    # FriendRequestListSerializer,
    # FriendRequestCreateSerializer,
    # FriendRequestDeleteSerializer,
) 

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsOwnerOrReadOnly

from rest_framework.response import Response


class ProfileListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.exclude(user=self.request.user)


class ProfileDetailAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    lookup_field = 'slug'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

  
# # Friend Requests API views
# class FriendRequestListAPIView(ListAPIView):
#     queryset = FriendRequest.objects.all()
#     serializer_class = FriendRequestListSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

# class FriendRequestCreateAPIView(CreateAPIView):
#     serializer_class = FriendRequestCreateSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def create(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class FriendRequestDeleteAPIView(DestroyAPIView):
#     serializer_class = FriendRequestDeleteSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
