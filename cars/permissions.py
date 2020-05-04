from rest_framework import permissions


class IsCarOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print('edw')
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print(' to change' ,obj, 'request', request.user)
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        print(request)

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
