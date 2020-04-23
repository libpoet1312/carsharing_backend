from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Gives write access only to the owner of the object.
    """
    #
    # def has_permission(self, request, view):
    #     if request.method in permissions.SAFE_METHODS:
    #         print('edw')
    #         return True

    def has_object_permission(self, request, view, obj):
        print('uploader=', obj.uploader)
        return obj.uploader == request.user
