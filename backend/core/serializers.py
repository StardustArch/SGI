# Ficheiro: backend/core/serializers.py
from rest_framework import serializers
from .models import Utilizador, Mensalidade, Sancao, Estudante,  PresencaEstudo

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