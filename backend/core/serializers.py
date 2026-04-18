from rest_framework import serializers
from django.utils import timezone
from .models import (
    Utilizador, Mensalidade, Sancao, Estudante,
    PresencaEstudo, PedidoSaida, Encarregado, Quarto,
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# ---------------------------------------------------------------------------
# UTILIZADOR
# ---------------------------------------------------------------------------
class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request=request, username=email, password=password)
        if user is None:
            raise serializers.ValidationError('Credenciais inválidas')
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    perfil_nome = serializers.SerializerMethodField()
    precisa_mudar_senha = serializers.SerializerMethodField()

    class Meta:
        model = Utilizador
        fields = ['id', 'email', 'first_name', 'last_name', 'perfil', 'perfil_nome', 'precisa_mudar_senha']

    def get_perfil_nome(self, obj):
        return obj.perfil.nome_perfil if obj.perfil else None

    def get_precisa_mudar_senha(self, obj):
        return obj.check_password('mudar1234')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("A senha antiga está incorrecta.")
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uidb64']))
            User = get_user_model()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Link de redefinição inválido ou expirado.")
        if not PasswordResetTokenGenerator().check_token(user, attrs['token']):
            raise serializers.ValidationError("Token inválido ou expirado.")
        attrs['user'] = user
        return attrs


# ---------------------------------------------------------------------------
# REGISTO COMPLETO
# ---------------------------------------------------------------------------
class EncarregadoRegistoSerializer(serializers.Serializer):
    nome_completo = serializers.CharField(max_length=255)
    telefone_principal = serializers.CharField(max_length=20)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    parentesco = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    telefone_alternativo = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    bi = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    morada = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    profissao = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)


class EstudanteRegistoSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    nome_completo = serializers.CharField(max_length=255)
    curso = serializers.CharField(max_length=100)
    genero = serializers.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Feminino')])
    quarto = serializers.PrimaryKeyRelatedField(queryset=Quarto.objects.all())
    data_nascimento = serializers.DateField(required=False, allow_null=True)
    bi = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    telefone_pessoal = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    email_pessoal = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    morada = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    nome_mae = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    nome_pai = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    nuit = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    ano_lectivo = serializers.CharField(max_length=9, required=False, allow_blank=True, allow_null=True)
    nacionalidade = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    condicao_saude = serializers.CharField(required=False, allow_blank=True, allow_null=True)
class RegistoCompletoSerializer(serializers.Serializer):
    encarregado = EncarregadoRegistoSerializer()
    estudante = EstudanteRegistoSerializer()
    criar_usuario_encarregado = serializers.BooleanField(default=False, required=False)


# ---------------------------------------------------------------------------
# ESTUDANTE
# ---------------------------------------------------------------------------
class EstudanteListSerializer(serializers.ModelSerializer):
    encarregado_nome = serializers.CharField(source='encarregado.nome_completo', read_only=True)
    quarto_numero = serializers.CharField(source='quarto.numero', read_only=True, default='—')
    bloco = serializers.CharField(source='quarto.bloco', read_only=True)

    bi = serializers.CharField(read_only=True)
    telefone_pessoal = serializers.CharField(read_only=True)

    class Meta:
        model = Estudante
        fields = [
            'utilizador_id', 'nome_completo', 'quarto', 'quarto_numero',
            'curso', 'estado', 'genero', 'encarregado_nome',
            'bi', 'telefone_pessoal', 'bloco'
        ]


class EncarregadoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encarregado
        fields = [
            'id', 'nome_completo', 'parentesco', 'telefone_principal',
            'telefone_alternativo', 'email', 'bi', 'morada', 'profissao'  # NOVO
        ]


class EstudanteDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='utilizador.codigo_acesso', read_only=True)
    encarregado_nome = serializers.CharField(source='encarregado.nome_completo', read_only=True)
    quarto_numero = serializers.CharField(source='quarto.numero', read_only=True)
    encarregado = EncarregadoDetailSerializer(read_only=True)

    class Meta:
        model = Estudante
        fields = [
            'utilizador', 'email', 'nome_completo', 'genero', 'quarto', 'quarto_numero',
            'curso', 'estado', 'encarregado', 'encarregado_nome',
            'data_nascimento', 'bi', 'telefone_pessoal', 'email_pessoal',
            'morada', 'nome_mae', 'nome_pai',
            'nuit', 'ano_lectivo', 'nacionalidade', 'condicao_saude'  # NOVOS
        ]
        read_only_fields = ['utilizador', 'email', 'encarregado_nome', 'quarto_numero', 'encarregado']


class EstudantePerfilSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='utilizador.email', read_only=True)
    encarregado_nome = serializers.CharField(source='encarregado.nome_completo', read_only=True)
    encarregado_telefone = serializers.CharField(source='encarregado.telefone_principal', read_only=True)
    quarto_numero = serializers.CharField(source='quarto.numero', read_only=True, default='—')
    quarto_bloco = serializers.CharField(source='quarto.bloco', read_only=True, default='—')

    class Meta:
        model = Estudante
        fields = [
            'utilizador_id', 'email', 'nome_completo',
            'genero', 'quarto', 'quarto_numero', 'quarto_bloco',
            'curso', 'estado', 'encarregado_nome', 'encarregado_telefone',
        ]
        read_only_fields = fields


class TransferirQuartoSerializer(serializers.Serializer):
    quarto_destino = serializers.PrimaryKeyRelatedField(queryset=Quarto.objects.filter(estado='Activo'))


# ---------------------------------------------------------------------------
# MENSALIDADE
# ---------------------------------------------------------------------------
class MensalidadeSerializer(serializers.ModelSerializer):
    esta_em_atraso = serializers.BooleanField(read_only=True)

    class Meta:
        model = Mensalidade
        fields = [
            'id', 'estudante', 'mes_referencia', 'valor_pago',
            'data_pagamento_confirmado', 'metodo_pagamento',
            'referencia_comprovativo', 'estado', 'data_vencimento',
            'esta_em_atraso', 'numero_recibo', 'tipo'  # NOVO
        ]
        read_only_fields = ['estudante', 'esta_em_atraso', 'data_vencimento', 'numero_recibo']


class MensalidadeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensalidade
        fields = [
            'estado', 'data_pagamento_confirmado',
            'metodo_pagamento', 'referencia_comprovativo', 'valor_pago',
        ]


class MensalidadeAdminListSerializer(serializers.ModelSerializer):
    nome_estudante = serializers.CharField(source='estudante.nome_completo', read_only=True)
    estado_display = serializers.SerializerMethodField()

    class Meta:
        model = Mensalidade
        fields = [
            'id', 'nome_estudante',
            'mes_referencia', 'estado', 'estado_display', 'valor_pago',
        ]

    def get_estado_display(self, obj):
        if obj.estado == 'Pago':
            return 'Pago'
        hoje = timezone.now().date()
        if obj.data_vencimento and obj.data_vencimento < hoje:
            return 'Atraso'
        return 'Pendente'


class GerarMensalidadesLoteSerializer(serializers.Serializer):
    mes_referencia = serializers.DateField()
    valor_padrao = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0.0)

    def validate_mes_referencia(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Não é possível gerar mensalidades para meses futuros.")
        return value


# ---------------------------------------------------------------------------
# PRESENÇA
# ---------------------------------------------------------------------------
class PresencaEstudoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.CharField(source='estudante.nome_completo', read_only=True)

    class Meta:
        model = PresencaEstudo
        fields = ['id', 'estudante', 'estudante_nome', 'data_presenca', 'estado', 'periodo']  # NOVO campo periodo


class PresencaEstudoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresencaEstudo
        fields = ['estado', 'periodo']  # NOVO


class PresencaBatchSerializer(serializers.Serializer):
    data_presenca = serializers.DateField()
    periodo = serializers.ChoiceField(choices=PresencaEstudo.PERIODO_CHOICES, default='Manhã')  # NOVO
    ausentes_ids = serializers.ListField(child=serializers.IntegerField(), required=False, default=list)
    justificados_ids = serializers.ListField(child=serializers.IntegerField(), required=False, default=list)
    bloco = serializers.CharField(required=False, allow_blank=True)  # NOVO filtro por bloco

    def validate(self, data):
        ausentes = set(data.get('ausentes_ids', []))
        justificados = set(data.get('justificados_ids', []))
        if not ausentes.isdisjoint(justificados):
            raise serializers.ValidationError("Um estudante não pode estar em 'ausentes' e 'justificados' ao mesmo tempo.")
        return data


# ---------------------------------------------------------------------------
# SANÇÃO
# ---------------------------------------------------------------------------
class SancaoSerializer(serializers.ModelSerializer):
    estudante = serializers.PrimaryKeyRelatedField(queryset=Estudante.objects.all())

    class Meta:
        model = Sancao
        fields = [
            'id', 'estudante', 'admin_id_registo',
            'data_ocorrencia', 'descricao', 'tipo_sancao', 'notificado_encarregado',
        ]
        read_only_fields = ['admin_id_registo']


class SancaoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sancao
        fields = ['data_ocorrencia', 'descricao', 'tipo_sancao', 'notificado_encarregado']


# ---------------------------------------------------------------------------
# PEDIDO DE SAÍDA
# ---------------------------------------------------------------------------
class PedidoSaidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoSaida
        fields = [
            'id', 'estudante', 'data_submissao',
            'data_saida_pretendida', 'data_retorno_pretendida',
            'motivo', 'estado', 'admin_id_aprovacao', 'observacao_admin',
            'destino', 'cidade_destino', 'meio_transporte', 'motivo_rejeicao'  # NOVOS
        ]
        read_only_fields = [
            'estudante', 'data_submissao', 'estado',
            'admin_id_aprovacao', 'observacao_admin', 'motivo_rejeicao'  # estudante não pode editar motivo de rejeição
        ]


class PedidoSaidaListAdminSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.CharField(source='estudante.nome_completo', read_only=True)

    class Meta:
        model = PedidoSaida
        fields = [
            'id', 'estudante_nome', 'estudante',
            'data_submissao', 'data_saida_pretendida',
            'data_retorno_pretendida', 'motivo', 'estado',
        ]


class PedidoSaidaUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoSaida
        fields = ['estado', 'observacao_admin', 'motivo_rejeicao']

    def validate_estado(self, value):
        # Permitir também 'Autorizado' se houver justificativa
        if value not in ['Aguardando_Encarregado', 'Rejeitado', 'Autorizado']:
            raise serializers.ValidationError(
                "Estado inválido. Use 'Aguardando_Encarregado', 'Rejeitado' ou 'Autorizado' (com justificativa)."
            )
        return value

    def validate(self, attrs):
        if attrs.get('estado') == 'Autorizado' and not attrs.get('observacao_admin'):
            raise serializers.ValidationError(
                {"observacao_admin": "É obrigatório justificar a aprovação directa (ex: 'Encarregado autorizou por telefone')."}
            )
        return attrs


class PedidoSaidaEncarregadoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoSaida
        fields = ['estado', 'motivo_rejeicao']  # NOVO campo

    def validate_estado(self, value):
        if value not in ['Autorizado', 'Rejeitado']:
            raise serializers.ValidationError(
                "Acção inválida. Use 'Autorizado' para autorizar ou 'Rejeitado' para recusar."
            )
        return value


# ---------------------------------------------------------------------------
# ENCARREGADO
# ---------------------------------------------------------------------------
class EncarregadoAdminSerializer(serializers.ModelSerializer):
    educandos = serializers.StringRelatedField(many=True, source='estudantes', read_only=True)
    email_contacto = serializers.EmailField(source='email', read_only=True)

    class Meta:
        model = Encarregado
        fields = ['utilizador_id', 'nome_completo', 'telefone_principal', 'email_contacto', 'educandos']


class EncarregadoProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encarregado
        fields = ['telefone_principal', 'email_contacto']


# ---------------------------------------------------------------------------
# QUARTO
# ---------------------------------------------------------------------------
class QuartoSerializer(serializers.ModelSerializer):
    vagas_disponiveis = serializers.ReadOnlyField()

    class Meta:
        model = Quarto
        fields = [
            'id', 'numero', 'bloco', 'capacidade_maxima',
            'genero_permitido', 'estado', 'ocupacao_atual', 'vagas_disponiveis',
        ]
        read_only_fields = ['ocupacao_atual', 'vagas_disponiveis']