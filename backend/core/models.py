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
        ('Gestor', 'Gestor do Internato'),
        ('Financeiro', 'Administrador Financeiro'),
        ('Disciplinar', 'Responsável Disciplinar'),
        ('Suporte', 'Suporte Técnico'), # Este é o "Super Admin" atual
        # Os nossos utentes:
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

class Quarto(models.Model):
    """ Gestão física de alojamento e vagas. """
    GENERO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino')]
    ESTADO_CHOICES = [('Activo', 'Activo'), ('Manutenção', 'Em Manutenção'), ('Inactivo', 'Inactivo')]

    numero = models.CharField(max_length=10, unique=True)
    bloco = models.CharField(max_length=50) # Ex: Bloco A, Ala Sul
    capacidade_maxima = models.PositiveIntegerField()
    genero_permitido = models.CharField(max_length=1, choices=GENERO_CHOICES)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Activo')
    
    # Campo para facilitar consultas rápidas, como pede a monografia
    ocupacao_atual = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Quarto"
        verbose_name_plural = "Quartos"

    def __str__(self):
        return f"Quarto {self.numero} - {self.bloco} ({self.genero_permitido})"

    @property
    def vagas_disponiveis(self):
        return self.capacidade_maxima - self.ocupacao_atual

class Estudante(models.Model):
    """ O registo central do internato. """
    utilizador = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    encarregado = models.ForeignKey(Encarregado, on_delete=models.PROTECT)
    
    nome_completo = models.CharField(max_length=255)
    num_estudante = models.CharField(max_length=50, unique=True)
    
    # ---- ALTERAÇÕES AQUI ----
    GENERO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino')]
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES) # Novo campo necessário
    
    # De CharField para ForeignKey
    quarto = models.ForeignKey(
        'Quarto', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="estudantes"
    )
    # ------------------------- 

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
    data_vencimento = models.DateField(null=True, blank=True, help_text="Data de vencimento da mensalidade")

    def save(self, *args, **kwargs):
        # Se não definido, calcular automaticamente a partir do mês de referência
        if self.data_vencimento is None and self.mes_referencia:
            # Define vencimento como o último dia do mês
            ultimo_dia = calendar.monthrange(self.mes_referencia.year, self.mes_referencia.month)[1]
            self.data_vencimento = self.mes_referencia.replace(day=ultimo_dia)
        super().save(*args, **kwargs)

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
    TIPO_SANCAO_CHOICES = [
        ('Advertência Verbal', 'Advertência Verbal'),
        ('Trabalho Comunitário', 'Trabalho Comunitário'),
        ('Suspensão de Saída', 'Suspensão de Saída'),
        ('Outro', 'Outro'),
    ]
    # ---- MODIFIQUE ESTA LINHA ----
    tipo_sancao = models.CharField(
        max_length=100, 
        choices=TIPO_SANCAO_CHOICES # <-- Adicionar isto
    )
    data_ocorrencia = models.DateField()
    descricao = models.TextField()
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
    data_aprovacao_encarregado = models.DateField()
    motivo = models.TextField()
    
    ESTADO_CHOICES = [
        ('Pendente', 'Pendente (Admin)'), 
        ('Aguardando_Encarregado', 'Aprovado Admin (Falta Encarregado)'), 
        ('Autorizado', 'Autorizado (Final)'), 
        ('Rejeitado', 'Rejeitado')
    ]
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Pendente')
    data_aprovacao_encarregado = models.DateTimeField(null=True, blank=True)
    observacao_admin = models.TextField(null=True, blank=True)

class Recibo(models.Model):
    """ Registo de recibos gerados para pagamentos confirmados. """
    mensalidade = models.OneToOneField(
        Mensalidade,
        on_delete=models.CASCADE,
        related_name='recibo'
    )
    numero_recibo = models.CharField(max_length=50, unique=True)
    data_emissao = models.DateTimeField(auto_now_add=True)
    arquivo_pdf = models.FileField(upload_to='recibos/', blank=True, null=True)  # opcional

    def __str__(self):
        return f"Recibo {self.numero_recibo} - {self.mensalidade.estudante.nome_completo}"
    def gerar_numero_recibo():
        from .models import Recibo
        ano = timezone.now().year
        # Contar quantos recibos já foram gerados no ano
        ultimo = Recibo.objects.filter(
            numero_recibo__startswith=f"REC-{ano}-"
        ).order_by('-numero_recibo').first()
        if ultimo:
            # Extrair o número final (ex: REC-2025-0001 -> 1)
            num = int(ultimo.numero_recibo.split('-')[-1]) + 1
        else:
            num = 1
        return f"REC-{ano}-{num:04d}"