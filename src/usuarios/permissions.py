from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    message = "Você não tem permissão para realizar essas ações."

    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsGestor(permissions.BasePermission):

    message = 'Apenas usuários do tipo Gestor podem realizar esta ação.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.tipo_usuario == 'GESTOR'

class IsEmployeeOfThisBranchOrManager(permissions.BasePermission):
    message = "Você não tem permissão para acessar os recursos desta filial."

    def has_permission(self, request, view):
        empresa_pk = view.kwargs.get('empresa_pk')
        filial_pk = view.kwargs.get('filial_pk')
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if user.tipo_usuario == 'FUNCIONARIO':
            return user.filial_associada_id == int(filial_pk)
        
        if user.tipo_usuario == 'GESTOR':
            return user.empresa_administrada.filter(pk=empresa_pk).exists()

        return False

class UserCreationPermission(permissions.BasePermission):
    message = "Você não tem permissão para criar este tipo de usuário."

    def has_permission(self, request, view):
        if view.action != 'create':
            return True 

        tipo_usuario = request.data.get('tipo_usuario')

        if tipo_usuario == 'GESTOR':
            return True
        
        elif tipo_usuario == 'FUNCIONARIO':
            return request.user and request.user.is_authenticated and request.user.tipo_usuario == 'GESTOR'
        
        return False
    
class IsManagerOfParentCompany(permissions.BasePermission):

    message = "Você precisa ser um gestor desta empresa para realizar esta ação."

    def has_permission(self, request, view):
        user = request.user
        
        empresa_pk = view.kwargs.get('empresa_pk') or view.kwargs.get('pk')

        if not user or not user.is_authenticated or not empresa_pk:
            return False

        if user.is_superuser:
            return True

        return user.tipo_usuario == 'GESTOR' and user.empresa_administrada.filter(pk=empresa_pk).exists()

class IsOwnerOrManagerOfSameCompany(permissions.BasePermission):

    message = "Você não tem permissão para realizar esta ação neste usuário."

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True

        is_gestor = request.user.is_authenticated and request.user.tipo_usuario == 'GESTOR'
        is_target_funcionario = obj.tipo_usuario == 'FUNCIONARIO' and obj.filial_associada is not None

        if is_gestor and is_target_funcionario:
            empresa_do_funcionario = obj.filial_associada.empresa_matriz
            
            return request.user.empresa_administrada.filter(pk=empresa_do_funcionario.pk).exists()

        return False
