from rest_framework.permissions import BasePermission, SAFE_METHODS

class UsuarioPerfil(BasePermission):

    """ Chequea si el usuario tiene permisos """
    def has_object_permission(self, request, view, obj):
        """ Chequea si esta intentando editar su propio perfil """

        if request.method in SAFE_METHODS:
            return True

        return obj.id == request.user.id



        