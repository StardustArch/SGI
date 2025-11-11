# Ficheiro: backend/core/permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permissão customizada para permitir acesso apenas a utilizadores
    com o perfil de 'Administrador'.
    """

    def has_permission(self, request, view):
        # Verifica se o utilizador está autenticado E
        # se o perfil do utilizador (ligado ao token) está definido
        if not request.user or not request.user.is_authenticated or not request.user.perfil:
            return False
        
        # Permite apenas se o nome do perfil for 'Administrador'
        return request.user.perfil.nome_perfil == 'Administrador'

class IsEstudanteUser(permissions.BasePermission):
    """
    Permissão customizada para permitir acesso apenas a utilizadores
    com o perfil de 'Estudante'.
    """
    def has_permission(self, request, view):
        # Verifica se o utilizador está autenticado E tem um perfil
        if not request.user or not request.user.is_authenticated or not request.user.perfil:
            return False
        
        # Permite apenas se o nome do perfil for 'Estudante'
        return request.user.perfil.nome_perfil == 'Estudante'

# Ficheiro: backend/core/permissions.py
# ... (Manter IsEstudanteUser) ...

# --- ADICIONE ESTA NOVA CLASSE ---

class IsOwnerOfPedidoSaida(permissions.BasePermission):
    """
    Permissão para garantir que o estudante (ou encarregado)
    só pode ver os seus próprios pedidos.
    """
    def has_object_permission(self, request, view, obj):
        # 'obj' é o PedidoSaida
        # request.user.id é a PK do estudante logado
        return obj.estudante_id == request.user.id


# Ficheiro: backend/core/permissions.py
# ... (Manter IsEstudanteUser e IsOwnerOfPedidoSaida) ...

# --- ADICIONE ESTA NOVA CLASSE ---

class IsEncarregadoUser(permissions.BasePermission):
    """
    Permissão customizada para permitir acesso apenas a utilizadores
    com o perfil de 'Encarregado'.
    """
    def has_permission(self, request, view):
        # Verifica se o utilizador está autenticado E tem um perfil
        if not request.user or not request.user.is_authenticated or not request.user.perfil:
            return False
        
        # Permite apenas se o nome do perfil for 'Encarregado'
        return request.user.perfil.nome_perfil == 'Encarregado'