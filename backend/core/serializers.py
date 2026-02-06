# Ficheiro: backend/core/serializers.py
from rest_framework import serializers
from .models import Utilizador, Mensalidade, Sancao, Estudante, PresencaEstudo, PedidoSaida, Encarregado
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    """ Serializer para o nosso modelo Utilizador """
    precisa_mudar_senha = serializers.SerializerMethodField()
    class Meta:
        model = Utilizador
        # Campos que queremos retornar na API
        fields = ['id', 'email', 'first_name', 'last_name', 'perfil', 'precisa_mudar_senha']
        # O 'perfil' vai mostrar o ID do perfil
    def get_precisa_mudar_senha(self, obj):
        # Verifica se a senha atual é a padrão "mudar1234"
        return obj.check_password('mudar1234')

class EncarregadoRegistoSerializer(serializers.Serializer):
    """ Valida os dados de entrada para o Encarregado """
    email = serializers.EmailField()
    nome_completo = serializers.CharField(max_length=255)
    telefone_principal = serializers.CharField(max_length=20)
    
class EstudanteRegistoSerializer(serializers.Serializer):
    """ Valida os dados de entrada para o Estudante """
    email = serializers.EmailField()
    nome_completo = serializers.CharField(max_length=255)
    num_estudante = serializers.CharField(max_length=50)
    quarto = serializers.CharField(max_length=10)
    curso = serializers.CharField(max_length=100)

class RegistoCompletoSerializer(serializers.Serializer):
    """
    Serializer "mãe" que recebe o JSON completo com os 
    dois objectos (encarregado e estudante).
    """
    encarregado = EncarregadoRegistoSerializer()
    estudante = EstudanteRegistoSerializer()

class MensalidadeSerializer(serializers.ModelSerializer):
    """
    Serializer para LISTAR e CRIAR mensalidades.
    """
    class Meta:
        model = Mensalidade
        fields = [
            'id', 
            'estudante', 
            'mes_referencia', 
            'valor_pago', 
            'data_pagamento_confirmado', 
            'metodo_pagamento', 
            'referencia_comprovativo', 
            'estado'
        ]
        # O 'estudante' será preenchido automaticamente pela URL,
        # por isso não o pedimos no JSON de entrada.
        read_only_fields = ['estudante']

class MensalidadeUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer específico para o Admin ATUALIZAR (PATCH) 
    uma mensalidade e confirmar o pagamento.
    """
    class Meta:
        model = Mensalidade
        # O Admin só pode (e deve) alterar estes campos 
        # para confirmar um pagamento.
        fields = [
            'estado', 
            'data_pagamento_confirmado', 
            'metodo_pagamento', 
            'referencia_comprovativo',
            'valor_pago' # Permitir ajustar o valor
        ]

# Ficheiro: backend/core/serializers.py
# ... (Manter os serializers Mensalidade existentes) ...

# --- ADICIONE ESTE NOVO SERIALIZER ---

class SancaoSerializer(serializers.ModelSerializer):
    """
    Serializer para LISTAR e CRIAR Sanções (Ações Disciplinares).
    """
    class Meta:
        model = Sancao
        fields = [
            'id', 
            'estudante',
            'admin_id_registo',
            'data_ocorrencia', 
            'descricao', 
            'tipo_sancao',
            'notificado_encarregado'
        ]
        # O 'estudante' e 'admin' serão preenchidos automaticamente.
        read_only_fields = ['estudante', 'admin_id_registo']


# Ficheiro: backend/core/serializers.py
# ... (Manter o SancaoSerializer) ...

# --- ADICIONE ESTE NOVO SERIALIZER ---

class PresencaEstudoSerializer(serializers.ModelSerializer):
    """
    Serializer para LISTAR o histórico de presenças.
    """
    class Meta:
        model = PresencaEstudo
        fields = ['id', 'data_presenca', 'estado']

# ... (Manter o PresencaBatchSerializer) ...
# Ficheiro: backend/core/serializers.py
# ... (Manter os serializers Sancao existentes) ...

# --- ADICIONE ESTE NOVO SERIALIZER ---

class PresencaBatchSerializer(serializers.Serializer):
    """
    Serializer para validar o POST em lote (batch) das presenças.
    Não é um ModelSerializer porque não mapeia 1-para-1 com um modelo.
    """
    data_presenca = serializers.DateField()
    
    # Esperamos uma lista de IDs (chaves primárias)
    ausentes_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        required=False # Pode não haver ausentes
    )
    justificados_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        required=False # Pode não haver justificados
    )

    def validate(self, data):
        """
        Validação extra para garantir que um estudante não está
        em ambas as listas ao mesmo tempo.
        """
        ausentes = set(data.get('ausentes_ids', []))
        justificados = set(data.get('justificados_ids', []))

        if not ausentes.isdisjoint(justificados):
            raise serializers.ValidationError("Um estudante não pode estar ausente E justificado.")
        
        return data

# Ficheiro: backend/core/serializers.py
# ... (Manter os serializers PresencaBatch existentes) ...

# --- ADICIONE ESTE NOVO SERIALIZER ---

class EstudanteListSerializer(serializers.ModelSerializer):
    """
    Serializer para LISTAR os estudantes.
    Fornece os dados essenciais para o admin pesquisar.
    """
    # Para mostrar o nome do encarregado em vez do ID
    encarregado_nome = serializers.CharField(source='encarregado.nome_completo', read_only=True)
    
    class Meta:
        model = Estudante
        fields = [
            'utilizador_id', # Este é o ID principal (PK)
            'nome_completo', 
            'num_estudante',
            'quarto',
            'curso',
            'estado',
            'encarregado_nome'
        ]


# Ficheiro: backend/core/serializers.py
# ... (Manter o EstudanteListSerializer) ...

# --- ADICIONE ESTE NOVO SERIALIZER ---

class PedidoSaidaSerializer(serializers.ModelSerializer):
    """
    Serializer para o Estudante LISTAR e CRIAR os seus Pedidos de Saída.
    """
    class Meta:
        model = PedidoSaida
        fields = [
            'id',
            'estudante',
            'data_submissao',
            'data_saida_pretendida',
            'data_retorno_pretendida',
            'motivo',
            'estado',
            'admin_id_aprovacao', # Para o estudante ver quem aprovou
            'observacao_admin'    # Para o estudante ver o motivo da rejeição
        ]
        
        # O estudante só pode enviar as datas e o motivo.
        # O resto é preenchido pelo sistema.
        read_only_fields = [
            'estudante', 
            'data_submissao', 
            'estado', 
            'admin_id_aprovacao', 
            'observacao_admin'
        ]


# Ficheiro: backend/core/serializers.py
# ... (Manter o PedidoSaidaSerializer) ...

# --- ADICIONE ESTES NOVOS SERIALIZERS (PARA O ADMIN) ---

class PedidoSaidaListAdminSerializer(serializers.ModelSerializer):
    """
    Serializer para o Admin LISTAR todos os pedidos pendentes.
    Mostra o nome do estudante para contexto.
    """
    # Puxa o nome do estudante da relação
    estudante_nome = serializers.CharField(source='estudante.nome_completo', read_only=True)

    class Meta:
        model = PedidoSaida
        fields = [
            'id',
            'estudante_nome', # <-- Importante para o admin
            'estudante',
            'data_submissao',
            'data_saida_pretendida',
            'data_retorno_pretendida',
            'motivo',
            'estado'
        ]

class PedidoSaidaUpdateAdminSerializer(serializers.ModelSerializer):
    """
    Serializer para o Admin ATUALIZAR (Aprovar/Rejeitar) um pedido.
    """
    class Meta:
        model = PedidoSaida
        # O Admin só pode mudar o estado e adicionar uma observação
        fields = ['estado', 'observacao_admin']

        # Garante que o estado seja válido (não pode ser "Pendente")
        def validate_estado(self, value):
            if value not in ['Aprovado_Admin', 'Rejeitado']:
                raise serializers.ValidationError("Estado inválido. Use 'Aprovado_Admin' ou 'Rejeitado'.")
            return value


# Ficheiro: backend/core/serializers.py
# ... (Manter os serializers existentes) ...

# --- ADICIONE ESTE NOVO SERIALIZER ---

class FinanceiroSummarySerializer(serializers.Serializer):
    """
    Serializer para o nosso Dashboard de Relatório Financeiro.
    Não é um ModelSerializer porque não mapeia para um modelo.
    """
    total_arrecadado_mes = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_pendente_mes = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_estudantes_pendentes = serializers.IntegerField()
    mes_referencia = serializers.DateField()

class TopInfratoresSerializer(serializers.Serializer):
    """
    Serializer para o Relatório 'Top 5 Infratores'.
    Mostra os estudantes com mais sanções.
    """
    # A nossa 'query' (na view) vai gerar estes campos:
    
    # Mapeia o 'estudante' (ID) da query para 'estudante_id' no JSON
    estudante_id = serializers.IntegerField(source='estudante') 
    
    # Mapeia o 'estudante__nome_completo' da query
    nome_completo = serializers.CharField(source='estudante__nome_completo')
    
    # Mapeia o 'total_sancoes' que vamos 'anotar'
    total_sancoes = serializers.IntegerField()

# Ficheiro: backend/core/serializers.py
# ... (Manter o TopInfratoresSerializer) ...

# --- ADICIONE ESTE NOVO SERIALIZER ---

class TopAusentesSerializer(serializers.Serializer):
    """
    Serializer para o Relatório 'Top 5 Ausentes'.
    Mostra os estudantes com mais ausências/justificações.
    """
    estudante_id = serializers.IntegerField(source='estudante')
    nome_completo = serializers.CharField(source='estudante__nome_completo')
    total_ausencias = serializers.IntegerField()

# Ficheiro: backend/core/serializers.py
# ... (Manter o TopAusentesSerializer) ...

# --- ADICIONE ESTE NOVO SERIALIZER ---

class TipoSancaoSummarySerializer(serializers.Serializer):
    """
    Serializer para o Relatório 'Sanções por Tipo'.
    Mostra o total de cada tipo de sanção.
    """
    tipo_sancao = serializers.CharField()
    total = serializers.IntegerField()

# Ficheiro: backend/core/serializers.py
# ... (Manter o TipoSancaoSummarySerializer) ...

# --- ADICIONE ESTE NOVO SERIALIZER ---

class PedidoSaidaSummarySerializer(serializers.Serializer):
    """
    Serializer para o Relatório 'Sumário de Pedidos de Saída'.
    """
    total_pendentes = serializers.IntegerField()
    total_aprovados = serializers.IntegerField()
    total_rejeitados = serializers.IntegerField()


class EstudanteDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para GET (detalhe) e PATCH (update) de um Estudante.
    """
    # Puxa campos read-only do modelo Utilizador e Encarregado
    email = serializers.EmailField(source='utilizador.email', read_only=True)
    encarregado_nome = serializers.CharField(source='encarregado.nome_completo', read_only=True)

    class Meta:
        model = Estudante
        fields = [
            'utilizador',       # A PK (id do utilizador)
            'email',            # O email (read-only)
            'nome_completo',    # Editável
            'num_estudante',    # Editável
            'quarto',           # Editável
            'curso',            # Editável
            'estado',           # Editável (Activo/Inactivo)
            'encarregado',      # ID do encarregado (read-only)
            'encarregado_nome'  # Nome do encarregado (read-only)
        ]
        # O admin não pode mudar o ID do estudante, o email ou o encarregado
        # através deste endpoint.
        read_only_fields = ['utilizador', 'email', 'encarregado', 'encarregado_nome']

class SancaoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para o Admin ATUALIZAR (PATCH) uma sanção.
    """
    class Meta:
        model = Sancao
        # Campos que o admin pode editar
        fields = [
            'data_ocorrencia', 
            'descricao', 
            'tipo_sancao',
            'notificado_encarregado'
        ]

class PresencaEstudoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para o Admin ATUALIZAR (PATCH) um registo de presença.
    Permite apenas alterar o estado.
    """
    class Meta:
        model = PresencaEstudo
        # O Admin só pode (e deve) alterar o estado
        fields = ['estado']

class EstudantePerfilSerializer(serializers.ModelSerializer):
    """
    Serializer para o Estudante (logado) ver
    os seus próprios dados de perfil.
    """
    # Puxa campos read-only do modelo Utilizador e Encarregado
    email = serializers.EmailField(source='utilizador.email', read_only=True)
    encarregado_nome = serializers.CharField(source='encarregado.nome_completo', read_only=True)
    encarregado_telefone = serializers.CharField(source='encarregado.telefone_principal', read_only=True)

    class Meta:
        model = Estudante
        fields = [
            'utilizador_id',    # A PK
            'email',
            'nome_completo',
            'num_estudante',
            'quarto',
            'curso',
            'estado',
            'encarregado_nome',
            'encarregado_telefone'
        ]
        # O estudante não pode editar nenhum destes campos, só ler.
        read_only_fields = fields

# --- ADICIONE ESTE NOVO SERIALIZER ---

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para o endpoint de mudança de senha.
    Exige a senha antiga e a nova.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        """
        Valida se a 'old_password' fornecida é a correta.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("A sua senha antiga está incorreta.")
        return value

    def validate_new_password(self, value):
        """
        Valida a força da nova senha (pode ser melhorado com validadores do Django).
        """
        if len(value) < 8:
            raise serializers.ValidationError("A nova senha deve ter pelo menos 8 caracteres.")
        return value

    def save(self):
        """
        Define a nova senha para o utilizador.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class PedidoSaidaEncarregadoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para o Encarregado APROVAR ou REJEITAR a saída.
    """
    class Meta:
        model = PedidoSaida
        fields = ['estado']

    def validate_estado(self, value):
        # O Encarregado só pode passar para 'Autorizado' ou 'Rejeitado'
        if value not in ['Autorizado', 'Rejeitado']:
            raise serializers.ValidationError("Ação inválida. Só pode 'Autorizar' ou 'Rejeitar'.")
        return value

class EncarregadoProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Permite ao Encarregado atualizar os seus contactos.
    """
    class Meta:
        model = Encarregado
        fields = ['telefone_principal', 'email_contacto']



class PasswordResetRequestSerializer(serializers.Serializer):
    """ Valida o pedido de reset (apenas email) """
    email = serializers.EmailField()

    def validate_email(self, value):
        # Verificar se o utilizador existe
        User = get_user_model()
        if not User.objects.filter(email=value).exists():
            # Por segurança, não devemos dizer "este email não existe"
            # mas para desenvolvimento ajuda. Em produção, retorne sucesso na mesma.
            raise serializers.ValidationError("Não existe nenhum utilizador com este email.")
        return value

class SetNewPasswordSerializer(serializers.Serializer):
    """ Recebe o token, o ID codificado e a nova senha """
    password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')
        password = attrs.get('password')

        # 1. Descodificar o ID do utilizador
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            User = get_user_model()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Link de redefinição inválido ou expirado.")

        # 2. Verificar se o token é válido para este user
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Token inválido ou expirado.")

        # Se passou tudo, guardamos o user no contexto para usar no save/view
        attrs['user'] = user
        return attrs