from rest_framework import permissions

class IsGestor(permissions.BasePermission):
    message = 'Apenas usuários do tipo Gestor podem realizar esta ação.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.tipo_usuario == 'GESTOR'