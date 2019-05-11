from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Comment, UploadedImage, Gallery

from comment import serializers

from core.permissions import IsOwnerOrReadOnly
from comment.permissions import IsImageOrCommentOwnerElseReadOnly

class CommentViewSet(viewsets.ModelViewSet):
    """Manage comments in the database"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsImageOrCommentOwnerElseReadOnly,)

    # def get_queryset(self):
    #     """Return objects for the current authenticated user only"""
    #     # return self.queryset.filter(user=self.request.user)
    #     return self.queryset

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        # if self.action == 'retrieve':
        #     return serializers.CommentDetailSerializer

        # user won't be able to change the image of an already created
        # comment
        if self.request.method == 'PUT':
            return serializers.CommentUpdateSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)
