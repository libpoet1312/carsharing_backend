from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Gives write access only to the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            print('edw')
            return True
        print(obj.uploader)
        return obj.uploader == request.user
