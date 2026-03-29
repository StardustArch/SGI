# Ficheiro: backend/core/permissions.py
from rest_framework import permissions


# ---------------------------------------------------------------------------
# PERMISSÕES ADMINISTRATIVAS
# ---------------------------------------------------------------------------

class IsAdminUser(permissions.BasePermission):
    """
    Permissão geral para qualquer membro do staff administrativo.
    Permite acesso a Gestor, Financeiro, Disciplinar e Suporte.
    Útil para dashboards e endpoints partilhados por todos os funcionários.
    """
    PERFIS = ['Gestor', 'Financeiro', 'Disciplinar', 'Suporte']

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.perfil
            and request.user.perfil.nome_perfil in self.PERFIS
        )


class IsAnyAdminUser(permissions.BasePermission):
    """
    FIX: substitui o uso incorreto de múltiplas permissões em AND
    no ExportarRelatorioView.

    DRF aplica permission_classes com AND implícito — nenhum utilizador
    consegue ser Gestor E Financeiro E Disciplinar ao mesmo tempo.
    Esta permissão faz OR entre todos os perfis admin, que é o
    comportamento correcto para endpoints de exportação/relatórios.
    """
    PERFIS = ['Gestor', 'Financeiro', 'Disciplinar', 'Suporte']

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.perfil
            and request.user.perfil.nome_perfil in self.PERFIS
        )


class IsGestorOuSuporte(permissions.BasePermission):
    """
    Acesso restrito à Direcção do Internato e Suporte Técnico.
    Usado para: registar estudantes, gerir quartos, aprovar pedidos de saída.
    """
    PERFIS = ['Gestor', 'Suporte']

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.perfil
            and request.user.perfil.nome_perfil in self.PERFIS
        )


class IsFinanceiroOuSuporte(permissions.BasePermission):
    """
    Acesso ao Módulo Financeiro.
    Gestor tem acesso total; Financeiro e Suporte têm acesso ao módulo.
    """
    PERFIS = ['Financeiro', 'Gestor', 'Suporte']

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.perfil
            and request.user.perfil.nome_perfil in self.PERFIS
        )


class IsDisciplinarOuSuporte(permissions.BasePermission):
    """
    Acesso ao Módulo Disciplinar e Presenças.
    Gestor tem acesso total; Disciplinar e Suporte têm acesso ao módulo.
    """
    PERFIS = ['Disciplinar', 'Gestor', 'Suporte']

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.perfil
            and request.user.perfil.nome_perfil in self.PERFIS
        )


# ---------------------------------------------------------------------------
# PERMISSÕES DE UTENTES
# ---------------------------------------------------------------------------

class IsEstudanteUser(permissions.BasePermission):
    """Permite acesso apenas a utilizadores com perfil 'Estudante'."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.perfil
            and request.user.perfil.nome_perfil == 'Estudante'
        )


class IsEncarregadoUser(permissions.BasePermission):
    """Permite acesso apenas a utilizadores com perfil 'Encarregado'."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.perfil
            and request.user.perfil.nome_perfil == 'Encarregado'
        )


class IsOwnerOfPedidoSaida(permissions.BasePermission):
    """
    Permissão a nível de objecto — garante que o estudante
    só consegue ver e agir sobre os seus próprios pedidos de saída.
    """

    def has_object_permission(self, request, view, obj):
        return obj.estudante_id == request.user.id