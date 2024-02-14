from rest_framework.permissions import BasePermission

# class IsModeratorOrIsOwner(BasePermission):
#    message = 'Вы не являетесь модератором или владельцем'
#    def has_permission(self, request, view):
#        if request.user.is_staff:
#            return True
#        return request.user == view.get_object().owner


class IsOwner(BasePermission):
    message = 'Вы не являетесь владельцем.'

    def has_permission(self, request, view):
        if request.user == view.get_object().owner:
            return True
