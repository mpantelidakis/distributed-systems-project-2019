from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class IsOwnderOrFriendOr403(permissions.BasePermission):
    """
    Custom permission to only allow friends of a user
    to interact with his galleries/images
    """

    message = 'You must add this user to your friends to access this object.'
    def has_object_permission(self, request, view, obj):
        # print('owner is: ', obj.owner)
        # print('request.user is: ', request.user)
        # print('Users friends profiles are:', request.user.profile.friends.all())

        if obj.owner == request.user:
            print("Permission granted, user is owner")
            return True
        for friend in request.user.profile.friends.all():
            if friend.user == obj.owner:
                print("Permission granted, user has followed owner")
                return True
        print("Permission denied, user has NOT followed owner")
        return False
