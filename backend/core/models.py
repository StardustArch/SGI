import calendar
from datetime import date
from dateutil.relativedelta import relativedelta  # NOVO: cálculo exato de idade
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils import timezone
from .utils import gerar_codigo_acesso


# ---------------------------------------------------------------------------
# MANAGER CUSTOMIZADO
# ---------------------------------------------------------------------------
class UtilizadorManager(BaseUserManager):
    def create_user(self, email=None, password=None, codigo_acesso=None, telefone=None, **extra_fields):
        if not email:
            email = ''
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if codigo_acesso:
            user.codigo_acesso = codigo_acesso
        elif telefone:
            user.telefone = telefone
        elif not user.codigo_acesso and not user.telefone:
            while True:
                novo = gerar_codigo_acesso()
                if not self.model.objects.filter(codigo_acesso=novo).exists():
                    user.codigo_acesso = novo
                    break
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


# ---------------------------------------------------------------------------
# PERFIS E UTILIZADOR
# ---------------------------------------------------------------------------
class Perfil(models.Model):
    NOME_CHOICES = [
        ('Gestor', 'Gestor do Internato'),
        ('Financeiro', 'Administrador Financeiro'),
        ('Disciplinar', 'Responsável Disciplinar'),
        ('Suporte', 'Suporte Técnico'),
        ('Estudante', 'Estudante'),
        ('Encarregado', 'Encarregado'),
    ]
    nome_perfil = models.CharField(max_length=50, choices=NOME_CHOICES, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_perfil


class Utilizador(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=True, null=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, blank=True)
    codigo_acesso = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Código de Acesso (estudantes)")
    telefone = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Telefone (encarregados)")

    groups = models.ManyToManyField('auth.Group', related_name='utilizador_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='utilizador_set', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UtilizadorManager()

    def __str__(self):
        return self.codigo_acesso or self.telefone or self.email or str(self.pk)


# ---------------------------------------------------------------------------
# ENCARREGADO
# ---------------------------------------------------------------------------
class Encarregado(models.Model):
    PARENTESCO_CHOICES = [
        ('Pai', 'Pai'),
        ('Mãe', 'Mãe'),
        ('Tio', 'Tio/Tia'),
        ('Irmão', 'Irmão/Irmã'),
        ('Avô', 'Avô/Avó'),
        ('Outro', 'Outro'),
    ]

    nome_completo = models.CharField(max_length=255)
    parentesco = models.CharField(max_length=20, choices=PARENTESCO_CHOICES, blank=True, null=True)
    telefone_principal = models.CharField(max_length=20, blank=False)
    telefone_alternativo = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    bi = models.CharField(max_length=20, blank=True, null=True)
    morada = models.TextField(blank=True, null=True)
    profissao = models.CharField(max_length=100, blank=True, null=True)  # NOVO CAMPO

    utilizador = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='encarregado_profile'
    )

    class Meta:
        verbose_name = "Encarregado / Contacto de Emergência"
        verbose_name_plural = "Encarregados"

    def __str__(self):
        return f"{self.nome_completo} ({self.parentesco or 'Sem parentesco'})"


# ---------------------------------------------------------------------------
# ESTUDANTE
# ---------------------------------------------------------------------------
class Estudante(models.Model):
    GENERO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino')]
    ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo')]

    utilizador = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    encarregado = models.ForeignKey(
        Encarregado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='estudantes'
    )
    nome_completo = models.CharField(max_length=255)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    quarto = models.ForeignKey('Quarto', on_delete=models.SET_NULL, null=True, blank=True, related_name='estudantes')
    curso = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')

    data_nascimento = models.DateField(null=True, blank=True)
    bi = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefone_pessoal = models.CharField(max_length=20, blank=True, null=True)
    email_pessoal = models.EmailField(blank=True, null=True)
    morada = models.TextField(blank=True, null=True)
    nome_mae = models.CharField(max_length=255, blank=True, null=True)
    nome_pai = models.CharField(max_length=255, blank=True, null=True)

    # NOVOS CAMPOS
    nuit = models.CharField(max_length=20, blank=True, null=True, verbose_name="NUIT")
    ano_lectivo = models.CharField(max_length=9, default='2025/2026', verbose_name="Ano Lectivo")
    nacionalidade = models.CharField(max_length=50, default='Moçambicana', blank=True)
    condicao_saude = models.TextField(blank=True, null=True, verbose_name="Condições de Saúde")

    @property
    def maior_de_idade(self):
        if not self.data_nascimento:
            return False
        # FIX: cálculo exato com relativedelta
        idade = relativedelta(date.today(), self.data_nascimento).years
        return idade >= 18

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarto_anterior_id = self.quarto_id

    def __str__(self):
        return self.nome_completo


# ---------------------------------------------------------------------------
# QUARTO
# ---------------------------------------------------------------------------
class Quarto(models.Model):
    GENERO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino')]
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Manutenção', 'Em Manutenção'),
        ('Inactivo', 'Inactivo'),
    ]

    numero = models.CharField(max_length=10, unique=True)
    bloco = models.CharField(max_length=50)
    capacidade_maxima = models.PositiveIntegerField()
    genero_permitido = models.CharField(max_length=1, choices=GENERO_CHOICES)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Activo')
    ocupacao_atual = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Quarto"
        verbose_name_plural = "Quartos"

    def __str__(self):
        return f"Quarto {self.numero} - {self.bloco} ({self.genero_permitido})"

    @property
    def vagas_disponiveis(self):
        return self.capacidade_maxima - self.ocupacao_atual

    def recalcular_ocupacao(self):
        self.ocupacao_atual = self.estudantes.filter(estado='Activo').count()
        self.save(update_fields=['ocupacao_atual'])


# ---------------------------------------------------------------------------
# MENSALIDADE
# ---------------------------------------------------------------------------
class Mensalidade(models.Model):
    METODO_CHOICES = [('Depósito', 'Depósito'), ('Numerário', 'Numerário')]
    ESTADO_CHOICES = [('Pendente', 'Pendente'), ('Pago', 'Pago')]
    TIPO_CHOICES = [                              # NOVO
        ('Inscrição', 'Inscrição'),
        ('Mensalidade', 'Mensalidade'),
    ]

    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='mensalidades')
    admin_id_registo = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='mensalidades_registadas'
    )
    mes_referencia = models.DateField()
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    data_pagamento_confirmado = models.DateField(null=True, blank=True)
    metodo_pagamento = models.CharField(max_length=20, choices=METODO_CHOICES, null=True, blank=True)
    referencia_comprovativo = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendente')
    data_vencimento = models.DateField(
        null=True, blank=True,
        help_text="Data de vencimento. Calculada automaticamente no save()."
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Mensalidade')  # NOVO

    numero_recibo = models.CharField(max_length=50, unique=True, null=True, blank=True)
    arquivo_pdf_recibo = models.FileField(upload_to='recibos/', blank=True, null=True)

    class Meta:
        unique_together = ('estudante', 'mes_referencia')

    def save(self, *args, **kwargs):
        # FIX: data de vencimento = dia 5 do mês seguinte
        if self.data_vencimento is None and self.mes_referencia:
            # dia 5 do mês seguinte
            if self.mes_referencia.month == 12:
                ano = self.mes_referencia.year + 1
                mes = 1
            else:
                ano = self.mes_referencia.year
                mes = self.mes_referencia.month + 1
            self.data_vencimento = date(ano, mes, 5)
        super().save(*args, **kwargs)

    @property
    def esta_em_atraso(self):
        if self.estado == 'Pendente' and self.data_vencimento:
            return self.data_vencimento < timezone.now().date()
        return False

    def __str__(self):
        return f"{self.estudante.nome_completo} — {self.mes_referencia}"


# ---------------------------------------------------------------------------
# PRESENÇA DE ESTUDO
# ---------------------------------------------------------------------------
class PresencaEstudo(models.Model):
    ESTADO_CHOICES = [
        ('Presente', 'Presente'),
        ('Ausente', 'Ausente'),
        ('Justificado', 'Justificado'),
    ]
    PERIODO_CHOICES = [                           # NOVO
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
        ('Noite', 'Noite'),
    ]

    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='presencas')
    admin_id_registo = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='presencas_registadas'
    )
    data_presenca = models.DateField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Presente')
    periodo = models.CharField(max_length=20, choices=PERIODO_CHOICES, default='Manhã')  # NOVO

    class Meta:
        unique_together = ('estudante', 'data_presenca', 'periodo')  # ajustado para incluir periodo

    def __str__(self):
        return f"{self.estudante.nome_completo} — {self.data_presenca} ({self.periodo}) — {self.estado}"


# ---------------------------------------------------------------------------
# SANÇÃO
# ---------------------------------------------------------------------------
class Sancao(models.Model):
    TIPO_SANCAO_CHOICES = [
        ('Advertência Verbal', 'Advertência Verbal'),
        ('Trabalho Comunitário', 'Trabalho Comunitário'),
        ('Suspensão de Saída', 'Suspensão de Saída'),
        ('Outro', 'Outro'),
    ]

    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='sancoes')
    admin_id_registo = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='sancoes_aplicadas'
    )
    tipo_sancao = models.CharField(max_length=100, choices=TIPO_SANCAO_CHOICES)
    data_ocorrencia = models.DateField()
    descricao = models.TextField()
    notificado_encarregado = models.BooleanField(default=False)

    def __str__(self):
        return f"Sanção — {self.estudante.nome_completo} — {self.data_ocorrencia}"


# ---------------------------------------------------------------------------
# PEDIDO DE SAÍDA
# ---------------------------------------------------------------------------
class PedidoSaida(models.Model):
    ESTADO_CHOICES = [
        ('Pendente', 'Pendente (Aguarda Admin)'),
        ('Aguardando_Encarregado', 'Aprovado Admin — Aguarda Encarregado'),
        ('Autorizado', 'Autorizado — Aprovado por todos'),
        ('Rejeitado', 'Rejeitado'),
    ]

    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='pedidos_saida')
    admin_id_aprovacao = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='pedidos_aprovados'
    )

    data_submissao = models.DateTimeField(auto_now_add=True)
    data_saida_pretendida = models.DateField()
    data_retorno_pretendida = models.DateField()
    motivo = models.TextField()
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Pendente')
    aprovado_por_sms = models.BooleanField(default=False)
    token_sms = models.CharField(max_length=6, blank=True, null=True)
    aprovado_presencialmente = models.BooleanField(default=False)

    data_aprovacao_encarregado = models.DateTimeField(null=True, blank=True)
    observacao_admin = models.TextField(null=True, blank=True)

    data_saida_real = models.DateTimeField(null=True, blank=True)
    data_regresso_real = models.DateTimeField(null=True, blank=True)

    # NOVOS CAMPOS
    destino = models.CharField(max_length=255, blank=True, null=True)
    cidade_destino = models.CharField(max_length=100, blank=True, null=True)
    meio_transporte = models.CharField(max_length=50, blank=True, null=True)
    motivo_rejeicao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido {self.pk} — {self.estudante.nome_completo} — {self.estado}"