# Ficheiro: backend/core/signals.py

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Sancao, Mensalidade, PedidoSaida, Utilizador

@receiver(post_save, sender=Sancao)
def enviar_notificacao_sancao(sender, instance, created, **kwargs):
    """
    Esta função é chamada automaticamente DEPOIS de uma 'Sancao' ser guardada.
    """

    # 'created' é True apenas na primeira vez que é guardada (criação).
    # Não queremos enviar um email se o admin estiver apenas a *editar* uma sanção antiga.
    if created:
        print(f"--- SINAL DETECTADO: Nova sanção ID {instance.id} criada ---")

        # Obter os objectos
        sancao = instance
        estudante = sancao.estudante
        encarregado = estudante.encarregado

        # Preparar o email
        subject = f"Notificação Disciplinar (SGI): {estudante.nome_completo}"
        message_body = f"""
        Exmo(a). Sr(a). {encarregado.nome_completo},

        Informamos que foi registada uma nova ocorrência disciplinar
        para o seu educando, {estudante.nome_completo}.

        Detalhes da Ocorrência:
        - Data: {sancao.data_ocorrencia}
        - Tipo: {sancao.tipo_sancao}
        - Descrição: {sancao.descricao}

        Para mais detalhes, por favor aceda ao portal SGI.

        Com os melhores cumprimentos,
        A Direcção do Internato IICB
        """

        # Enviar o email
        try:
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                [encarregado.email_contacto], # Lista de destinatários
                fail_silently=False,
            )
            print(f"--- Email de notificação enviado para {encarregado.email_contacto} ---")
        except Exception as e:
            print(f"--- ERRO AO ENVIAR EMAIL: {str(e)} ---")

# Ficheiro: backend/core/signals.py

# ... (manter a função enviar_notificacao_sancao) ...

# --- ADICIONE ESTA NOVA FUNÇÃO ---

@receiver(post_save, sender=Mensalidade)
def enviar_notificacao_pagamento(sender, instance, created, update_fields, **kwargs):
    """
    Envia um email de confirmação (recibo) quando uma mensalidade é
    actualizada (PATCH) para o estado 'Pago'.
    """
    
    # 1. Não fazer nada na *criação* (só em actualizações)
    if created:
        return

    # 2. Verificar se o 'estado' foi um dos campos actualizados
    #    e se o novo estado é 'Pago'.
    #    (Isto evita re-enviar emails se o admin só mudar o 'valor' de um
    #     pagamento que já estava Pago)
    if update_fields and 'estado' in update_fields and instance.estado == 'Pago':
        
        print(f"--- SINAL DETECTADO: Mensalidade ID {instance.id} foi Paga ---")
        
        mensalidade = instance
        estudante = mensalidade.estudante
        encarregado = estudante.encarregado
        
        # Preparar o email
        subject = f"Confirmação de Pagamento (SGI): {estudante.nome_completo}"
        message_body = f"""
        Exmo(a). Sr(a). {encarregado.nome_completo},
        
        Confirmamos a recepção do pagamento da mensalidade
        para o seu educando, {estudante.nome_completo}.
        
        Detalhes do Pagamento:
        - Mês de Referência: {mensalidade.mes_referencia.strftime('%B de %Y')}
        - Valor Pago: {mensalidade.valor_pago}
        - Data da Confirmação: {mensalidade.data_pagamento_confirmado}
        - Método: {mensalidade.metodo_pagamento}
        
        Obrigado,
        A Direcção do Internato IICB
        """
        
        # Enviar o email
        try:
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                [encarregado.email_contacto],
                fail_silently=False,
            )
            print(f"--- Email de recibo enviado para {encarregado.email_contacto} ---")
        except Exception as e:
            print(f"--- ERRO AO ENVIAR EMAIL DE RECIBO: {str(e)} ---")


# Ficheiro: backend/core/signals.py
# ... (manter a função enviar_notificacao_pagamento) ...

# --- OUVINTE 3: Novo Pedido de Saída ---

@receiver(post_save, sender=PedidoSaida)
def notificar_admin_novo_pedido_saida(sender, instance, created, **kwargs):
    """
    Envia um email ao(s) Admin(s) quando um novo pedido de
    saída é submetido por um estudante.
    """
    
    # Só dispara na *criação* de um novo pedido
    if created:
        print(f"--- SINAL DETECTADO: Novo Pedido de Saída ID {instance.id} criado ---")
        
        pedido = instance
        estudante = pedido.estudante
        
        # Obter os emails de TODOS os admins
        # (Isto assume que o seu superuser 'paulo@mail.com' tem o Perfil 'Administrador' atribuído)
        admin_emails = list(
            Utilizador.objects.filter(perfil__nome_perfil='Administrador')
                            .values_list('email', flat=True)
        )
        
        if not admin_emails:
            print("--- ERRO DE NOTIFICAÇÃO: Nenhum Admin encontrado para notificar. ---")
            return

        # Preparar o email
        subject = f"Novo Pedido de Saída Pendente (SGI): {estudante.nome_completo}"
        message_body = f"""
        Um novo pedido de saída foi submetido e aguarda aprovação.
        
        Detalhes do Pedido:
        - Estudante: {estudante.nome_completo} (ID: {estudante.pk})
        - Data de Saída: {pedido.data_saida_pretendida}
        - Data de Retorno: {pedido.data_retorno_pretendida}
        - Motivo: {pedido.motivo}
        
        Por favor, aceda ao painel de administração para aprovar ou rejeitar.
        """
        
        try:
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                admin_emails, # Envia para todos os admins
                fail_silently=False,
            )
            print(f"--- Email de Pedido Pendente enviado para: {', '.join(admin_emails)} ---")
        except Exception as e:
            print(f"--- ERRO AO ENVIAR EMAIL DE PEDIDO PENDENTE: {str(e)} ---")


# Ficheiro: backend/core/signals.py
# ... (manter a função notificar_admin_novo_pedido_saida) ...

# --- OUVINTE 4: Resposta ao Pedido de Saída ---

@receiver(post_save, sender=PedidoSaida)
def notificar_estudante_resposta_pedido(sender, instance, created, update_fields, **kwargs):
    """
    Envia um email ao Estudante quando o seu pedido de saída
    é Aprovado ou Rejeitado pelo Admin.
    """
    
    # 1. Não fazer nada na *criação*
    if created:
        return

    # 2. Só disparar se o 'estado' foi actualizado
    if update_fields and 'estado' in update_fields:
        
        # 3. Verificar se o novo estado é um estado final
        if instance.estado in ['Aprovado_Admin', 'Rejeitado']:
            
            print(f"--- SINAL DETECTADO: Pedido ID {instance.id} foi respondido ---")
            
            pedido = instance
            estudante = pedido.estudante
            
            # Formatar o estado para ser legível (ex: "Aprovado_Admin" -> "Aprovado")
            estado_legivel = "Aprovado" if instance.estado == 'Aprovado_Admin' else "Rejeitado"

            # Preparar o email
            subject = f"Resposta ao seu Pedido de Saída (SGI): {estado_legivel}"
            message_body = f"""
            Olá {estudante.nome_completo},
            
            O seu pedido de saída (ID {pedido.id}) foi respondido pela administração.
            
            Detalhes do Pedido:
            - Data de Saída: {pedido.data_saida_pretendida}
            - Data de Retorno: {pedido.data_retorno_pretendida}
            - Motivo: {pedido.motivo}
            
            Resultado:
            - Novo Estado: {estado_legivel}
            - Observação do Admin: {pedido.observacao_admin or "N/A"}
            
            Com os melhores cumprimentos,
            A Direcção do Internato IICB
            """
            
            try:
                send_mail(
                    subject,
                    message_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [estudante.utilizador.email], # Envia para o email de login do estudante
                    fail_silently=False,
                )
                print(f"--- Email de Resposta de Pedido enviado para: {estudante.utilizador.email} ---")
            except Exception as e:
                print(f"--- ERRO AO ENVIAR EMAIL DE RESPOSTA DE PEDIDO: {str(e)} ---")