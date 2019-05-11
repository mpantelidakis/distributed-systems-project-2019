from rest_framework import permissions


class IsImageOrCommentOwnerElseReadOnly(permissions.BasePermission):
    """
    Custom permission to allow owners of a comment to delete or edit it.
    Moreover the owner of the image to which the comment is attached
    can ONLY delete the comment
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            return ((obj.owner == request.user) | (obj.image.owner == request.user)) 

        # Update permissions are only allowed to the owner of the comment.
        return obj.owner == request.user
