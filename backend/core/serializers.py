# Ficheiro: backend/core/serializers.py
from rest_framework import serializers
from .models import Utilizador, Mensalidade, Sancao, Estudante, PresencaEstudo, PedidoSaida

class UserSerializer(serializers.ModelSerializer):
    """ Serializer para o nosso modelo Utilizador """
    class Meta:
        model = Utilizador
        # Campos que queremos retornar na API
        fields = ['id', 'email', 'first_name', 'last_name', 'perfil']
        # O 'perfil' vai mostrar o ID do perfil

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