from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings
# -----------------------------------------------------------
# 1. **** ADICIONAR ESTE NOVO MANAGER ****
# (Manager para corrigir o erro 'createsuperuser')
# -----------------------------------------------------------
class UtilizadorManager(BaseUserManager):
    """
    Manager customizado onde o email é o identificador único
    em vez do username.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um Utilizador com o email e password.
        """
        if not email:
            raise ValueError('O Email deve ser definido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e salva um SuperUtilizador com o email e password.
        O comando 'createsuperuser' vai chamar este método.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # O comando 'createsuperuser' passa o email.
        # Nós passamos para o nosso 'create_user' helper.
        return self.create_user(email, password, **extra_fields)

# -----------------------------------------------------------
# 2. MODELOS DE PERFIS E UTILIZADOR
# -----------------------------------------------------------

class Perfil(models.Model):
    """ Tabela de 'Roles' (Perfis) para definir permissões. """
    NOME_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Estudante', 'Estudante'),
        ('Encarregado', 'Encarregado'),
    ]
    nome_perfil = models.CharField(max_length=50, choices=NOME_CHOICES, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_perfil

class Utilizador(AbstractUser):
    """
    Modelo de Utilizador customizado.
    """
    # **** ALTERAÇÃO ****
    # Remover o campo username herdado, já que não o usamos.
    username = None 

    # Manter email como único e principal
    email = models.EmailField(unique=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Manter as correcções de 'related_name'
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilizador_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilizador_set',
        blank=True,
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Note que 'email' NÃO está aqui

    # **** ALTERAÇÃO ****
    # Ligar o nosso novo manager
    objects = UtilizadorManager() 

    def __str__(self):
        return self.email

class Encarregado(models.Model):
    """ Dados de perfil do Encarregado. """
    # Ligação 1-para-1 com o Utilizador (só 1 login por encarregado)
    utilizador = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    nome_completo = models.CharField(max_length=255)
    telefone_principal = models.CharField(max_length=20, unique=True)
    email_contacto = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome_completo

class Estudante(models.Model):
    """ O registo central do internato. """
    # Ligação 1-para-1 com o Utilizador (só 1 login por estudante)
    utilizador = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    encarregado = models.ForeignKey(Encarregado, on_delete=models.PROTECT) # Proteger: não apagar encarregado se tiver estudante
    
    nome_completo = models.CharField(max_length=255)
    num_estudante = models.CharField(max_length=50, unique=True)
    quarto = models.CharField(max_length=10)
    curso = models.CharField(max_length=100)
    
    ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo')]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')

    def __str__(self):
        return self.nome_completo

# -----------------------------------------------------------
# 2. MÓDULOS DE GESTÃO (FINANCEIRO, DISCIPLINA, ETC.)
# -----------------------------------------------------------

class Mensalidade(models.Model):
    """ O módulo financeiro (substitui o Excel). """
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name="mensalidades")
    admin_id_registo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="mensalidades_registadas")
    
    mes_referencia = models.DateField() # Ex: 2025-11-01
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    data_pagamento_confirmado = models.DateField(null=True, blank=True)
    
    METODO_CHOICES = [('Depósito', 'Depósito'), ('Numerário', 'Numerário')]
    metodo_pagamento = models.CharField(max_length=20, choices=METODO_CHOICES, null=True, blank=True)
    referencia_comprovativo = models.CharField(max_length=100, null=True, blank=True)
    
    ESTADO_CHOICES = [('Pendente', 'Pendente'), ('Pago', 'Pago')]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendente')

    class Meta:
        unique_together = ('estudante', 'mes_referencia') # Não permite 2 registos para o mesmo mês/estudante

class PresencaEstudo(models.Model):
    """ Registo de presenças nos estudos obrigatórios. """
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name="presencas")
    admin_id_registo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="presencas_registadas")
    
    data_presenca = models.DateField()
    ESTADO_CHOICES = [('Presente', 'Presente'), ('Ausente', 'Ausente'), ('Justificado', 'Justificado')]
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Presente')

    class Meta:
        unique_together = ('estudante', 'data_presenca')

class Sancao(models.Model):
    """ Histórico disciplinar do estudante. """
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name="sancoes")
    admin_id_registo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="sancoes_aplicadas")
    
    data_ocorrencia = models.DateField()
    descricao = models.TextField()
    tipo_sancao = models.CharField(max_length=100) # Ex: 'Advertência Verbal'
    notificado_encarregado = models.BooleanField(default=False)

    def __str__(self):
        return f"Sanção para {self.estudante.nome_completo} em {self.data_ocorrencia}"

class PedidoSaida(models.Model):
    """ Fluxo digital para pedidos de saída. """
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name="pedidos_saida")
    admin_id_aprovacao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="pedidos_aprovados")
    
    data_submissao = models.DateTimeField(auto_now_add=True)
    data_saida_pretendida = models.DateField()
    data_retorno_pretendida = models.DateField()
    motivo = models.TextField()
    
    ESTADO_CHOICES = [('Pendente', 'Pendente'), ('Aprovado_Admin', 'Aprovado (Admin)'), ('Rejeitado', 'Rejeitado')]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendente')
    observacao_admin = models.TextField(null=True, blank=True)