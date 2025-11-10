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