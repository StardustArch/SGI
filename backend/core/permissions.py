# Ficheiro: backend/core/permissions.py
from rest_framework import permissions

# -----------------------------------------------------------
# PERMISSÕES ADMINISTRATIVAS (Monografia)
# -----------------------------------------------------------

class IsAdminUser(permissions.BasePermission):
    """
    Permissão GERAL para qualquer membro do staff.
    Permite o acesso se for Gestor, Financeiro, Disciplinar ou Suporte.
    (Útil para dashboards gerais onde todos os funcionários entram).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or not request.user.perfil:
            return False
        
        perfis_admin = ['Gestor', 'Financeiro', 'Disciplinar', 'Suporte', 'Administrador']
        return request.user.perfil.nome_perfil in perfis_admin


class IsGestorOuSuporte(permissions.BasePermission):
    """
    Acesso restrito à Direção do Internato e Suporte Técnico.
    (Ex: Registar novos estudantes, ver relatórios globais).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or not request.user.perfil:
            return False
        
        return request.user.perfil.nome_perfil in ['Gestor', 'Suporte', 'Administrador']


class IsFinanceiroOuSuporte(permissions.BasePermission):
    """
    Acesso ao Módulo Financeiro.
    Apenas o Administrador Financeiro, Gestor e Suporte.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or not request.user.perfil:
            return False
        
        return request.user.perfil.nome_perfil in ['Financeiro', 'Gestor', 'Suporte', 'Administrador']


class IsDisciplinarOuSuporte(permissions.BasePermission):
    """
    Acesso ao Módulo Disciplinar e Presenças.
    Apenas o Responsável Disciplinar, Gestor e Suporte.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or not request.user.perfil:
            return False
        
        return request.user.perfil.nome_perfil in ['Disciplinar', 'Gestor', 'Suporte', 'Administrador']


# -----------------------------------------------------------
# PERMISSÕES DE UTENTES (Estudante & Encarregado)
# -----------------------------------------------------------

class IsEstudanteUser(permissions.BasePermission):
    """
    Permite acesso apenas a utilizadores com o perfil de 'Estudante'.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or not request.user.perfil:
            return False
        return request.user.perfil.nome_perfil == 'Estudante'


class IsEncarregadoUser(permissions.BasePermission):
    """
    Permite acesso apenas a utilizadores com o perfil de 'Encarregado'.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or not request.user.perfil:
            return False
        return request.user.perfil.nome_perfil == 'Encarregado'


class IsOwnerOfPedidoSaida(permissions.BasePermission):
    """
    Garante que o estudante só pode ver os seus próprios pedidos.
    """
    def has_object_permission(self, request, view, obj):
        return obj.estudante_id == request.user.id