"""
signals.py — SGI Internato IICB

Responsabilidades:
  1. Manter ocupacao_atual do Quarto sempre consistente (via post_save/post_delete do Estudante)
  2. Notificar encarregado quando há nova sanção
  3. Confirmar pagamento ao encarregado quando mensalidade passa a 'Pago'
  4. Notificar admin sobre novo pedido de saída
  5. Notificar estudante sobre resposta ao pedido de saída

Estratégia de notificação:
  - Modo LOCAL_MODE=True (LAN sem internet): notificações só em log/consola
  - Modo produção: tenta SMS via AfricasTalking; fallback para email se configurado
  - Nunca lança excepção — falha silenciosa com log, para não bloquear operações críticas
"""

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from .models import Estudante, Sancao, Mensalidade, PedidoSaida, Utilizador

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# HELPERS DE NOTIFICAÇÃO
# ---------------------------------------------------------------------------


def _enviar_sms(telefone: str, mensagem: str) -> bool:
    """
    Envia SMS via AfricasTalking (presença confirmada em Moçambique).
    Retorna True se enviou, False se falhou ou não está configurado.
    Instalar: pip install africastalking
    """
    at_username = getattr(settings, "AT_USERNAME", None)
    at_api_key = getattr(settings, "AT_API_KEY", None)

    if not at_username or not at_api_key:
        logger.info(f"[SMS-SKIP] SMS não configurado. Mensagem: {mensagem[:60]}...")
        return False

    try:
        import africastalking

        africastalking.initialize(at_username, at_api_key)
        sms = africastalking.SMS
        response = sms.send(mensagem, [telefone])
        logger.info(f"[SMS-OK] Enviado para {telefone}: {response}")
        return True
    except ImportError:
        logger.warning(
            "[SMS-SKIP] africastalking não instalado. pip install africastalking"
        )
        return False
    except Exception as e:
        logger.error(f"[SMS-ERRO] Falha ao enviar para {telefone}: {e}")
        return False


def _enviar_email(destinatario: str, assunto: str, corpo: str) -> bool:
    """
    Fallback de email. Só envia se o encarregado tiver email e
    o backend não for console (produção real).
    """
    if not destinatario:
        return False

    # Em LOCAL_MODE, email vai para consola (útil para debug)
    from django.core.mail import send_mail

    try:
        send_mail(
            assunto,
            corpo,
            settings.DEFAULT_FROM_EMAIL,
            [destinatario],
            fail_silently=False,
        )
        logger.info(f"[EMAIL-OK] Enviado para {destinatario}")
        return True
    except Exception as e:
        logger.error(f"[EMAIL-ERRO] Falha ao enviar para {destinatario}: {e}")
        return False


def _notificar_encarregado(
    encarregado, assunto: str, mensagem_sms: str, corpo_email: str
):
    """
    Tenta SMS primeiro (realista para Moçambique).
    Se não tiver SMS configurado, tenta email como fallback.
    """
    telefone = getattr(encarregado, "telefone_principal", None)
    email = getattr(encarregado, "email_contacto", None)

    sms_enviado = _enviar_sms(telefone, mensagem_sms) if telefone else False

    if not sms_enviado and email:
        _enviar_email(email, assunto, corpo_email)


# ---------------------------------------------------------------------------
# SIGNAL 1 — Ocupação do Quarto (CRÍTICO para consistência de dados)
# Resolve o bug onde ocupacao_atual só incrementava mas nunca decrementava.
# ---------------------------------------------------------------------------


@receiver(post_save, sender=Estudante)
def actualizar_ocupacao_no_save(sender, instance, created, **kwargs):
    """
    Recalcula a ocupação do quarto sempre que um Estudante é guardado.
    Cobre: criação, mudança de quarto, activação/desactivação.
    """
    # Recalcular quarto actual (se tiver)
    if instance.quarto:
        instance.quarto.recalcular_ocupacao()

    # Se é uma actualização (não criação), pode ter mudado de quarto —
    # precisamos de recalcular o quarto ANTERIOR também.
    # Para isso guardamos o quarto anterior no __init__ do modelo.
    quarto_anterior_id = getattr(instance, "_quarto_anterior_id", None)
    if quarto_anterior_id and quarto_anterior_id != getattr(
        instance.quarto, "pk", None
    ):
        from .models import Quarto

        try:
            quarto_anterior = Quarto.objects.get(pk=quarto_anterior_id)
            quarto_anterior.recalcular_ocupacao()
        except Quarto.DoesNotExist:
            pass


@receiver(post_delete, sender=Estudante)
def actualizar_ocupacao_no_delete(sender, instance, **kwargs):
    """Recalcula a ocupação quando um Estudante é removido."""
    if instance.quarto:
        instance.quarto.recalcular_ocupacao()


# ---------------------------------------------------------------------------
# SIGNAL 2 — Nova Sanção: notificar encarregado
# ---------------------------------------------------------------------------


@receiver(post_save, sender=Sancao)
def notificar_sancao(sender, instance, created, **kwargs):
    """Notifica o encarregado quando é criada uma nova sanção."""
    if not created:
        return

    sancao = instance
    estudante = sancao.estudante
    encarregado = estudante.encarregado

    logger.info(f"[SINAL] Nova sanção ID={sancao.id} para {estudante.nome_completo}")

    assunto = f"[SGI-IICB] Ocorrência disciplinar — {estudante.nome_completo}"

    mensagem_sms = (
        f"IICB Internato: O seu educando {estudante.nome_completo} "
        f"recebeu uma ocorrência disciplinar ({sancao.tipo_sancao}) "
        f"em {sancao.data_ocorrencia}. Contacte a direcção para mais info."
    )

    corpo_email = f"""
Exmo(a). Sr(a). {encarregado.nome_completo},

Foi registada uma ocorrência disciplinar para o seu educando.

Estudante: {estudante.nome_completo}
Data: {sancao.data_ocorrencia}
Tipo: {sancao.tipo_sancao}
Descrição: {sancao.descricao}

Para mais detalhes, contacte a direcção do Internato IICB.

Com os melhores cumprimentos,
Direcção do Internato — IICB
    """

    _notificar_encarregado(encarregado, assunto, mensagem_sms, corpo_email)

    # Marcar como notificado para rastreabilidade
    Sancao.objects.filter(pk=sancao.pk).update(notificado_encarregado=True)


# ---------------------------------------------------------------------------
# SIGNAL 3 — Mensalidade paga: confirmar ao encarregado
# ---------------------------------------------------------------------------


@receiver(post_save, sender=Mensalidade)
def confirmar_pagamento(sender, instance, created, update_fields, **kwargs):
    """
    Envia confirmação quando uma mensalidade passa para 'Pago'.
    Só dispara em actualizações onde o campo 'estado' foi explicitamente alterado.
    """
    if created:
        return

    # Só actua se 'estado' estiver nos campos actualizados E for 'Pago'
    if update_fields and "estado" in update_fields and instance.estado == "Pago":
        mensalidade = instance
        estudante = mensalidade.estudante
        encarregado = estudante.encarregado

        logger.info(f"[SINAL] Mensalidade ID={mensalidade.id} marcada como Paga")

        assunto = f"[SGI-IICB] Pagamento confirmado — {estudante.nome_completo}"

        mensagem_sms = (
            f"IICB Internato: Pagamento de {mensalidade.valor_pago} MZN "
            f"referente a {mensalidade.mes_referencia.strftime('%m/%Y')} "
            f"de {estudante.nome_completo} confirmado. Obrigado."
        )

        corpo_email = f"""
Exmo(a). Sr(a). {encarregado.nome_completo},

Confirmamos a recepção do pagamento do seu educando.

Estudante: {estudante.nome_completo}
Mês: {mensalidade.mes_referencia.strftime('%B de %Y')}
Valor Pago: {mensalidade.valor_pago} MZN
Data de Confirmação: {mensalidade.data_pagamento_confirmado}
Método: {mensalidade.metodo_pagamento}
Referência: {mensalidade.referencia_comprovativo or 'N/A'}

Com os melhores cumprimentos,
Direcção do Internato — IICB
        """

        _notificar_encarregado(encarregado, assunto, mensagem_sms, corpo_email)


# ---------------------------------------------------------------------------
# SIGNAL 4 — Novo pedido de saída: notificar admins
# ---------------------------------------------------------------------------


@receiver(post_save, sender=PedidoSaida)
def notificar_admins_novo_pedido(sender, instance, created, **kwargs):
    """Notifica todos os Gestores quando há um novo pedido de saída."""
    if not created:
        return

    pedido = instance
    estudante = pedido.estudante

    logger.info(
        f"[SINAL] Novo pedido de saída ID={pedido.id} de {estudante.nome_completo}"
    )

    # Notificar todos os admins com email cadastrado
    admin_emails = list(
        Utilizador.objects.filter(perfil__nome_perfil__in=["Gestor", "Suporte"])
        .exclude(email="")
        .values_list("email", flat=True)
    )

    if not admin_emails:
        logger.warning("[SINAL] Nenhum Gestor/Suporte com email para notificar.")
        return

    assunto = f"[SGI-IICB] Novo pedido de saída — {estudante.nome_completo}"
    corpo = f"""
Novo pedido de saída submetido e a aguardar aprovação.

Estudante: {estudante.nome_completo}
Saída pretendida: {pedido.data_saida_pretendida}
Retorno pretendido: {pedido.data_retorno_pretendida}
Motivo: {pedido.motivo}

Aceda ao painel de administração para aprovar ou rejeitar.
    """

    for email in admin_emails:
        _enviar_email(email, assunto, corpo)


# ---------------------------------------------------------------------------
# SIGNAL 5 — Resposta do admin ao pedido: notificar estudante
# ---------------------------------------------------------------------------


@receiver(post_save, sender=PedidoSaida)
def notificar_estudante_resposta(sender, instance, created, update_fields, **kwargs):
    """
    Notifica o estudante quando o admin responde ao pedido.
    Dispara quando estado muda para 'Aguardando_Encarregado' ou 'Rejeitado'.
    """
    if created:
        return

    if not (update_fields and "estado" in update_fields):
        return

    if instance.estado not in ["Aguardando_Encarregado", "Rejeitado"]:
        return

    pedido = instance
    estudante = pedido.estudante
    email_estudante = estudante.utilizador.email

    if instance.estado == "Aguardando_Encarregado":
        resultado = "aprovado pela administração e aguarda confirmação do encarregado"
    else:
        resultado = "rejeitado pela administração"

    assunto = (
        f"[SGI-IICB] Pedido de saída {instance.estado} — {estudante.nome_completo}"
    )
    corpo = f"""
Olá {estudante.nome_completo},

O seu pedido de saída (ID {pedido.id}) foi {resultado}.

Saída pretendida: {pedido.data_saida_pretendida}
Retorno pretendido: {pedido.data_retorno_pretendida}
Observação da administração: {pedido.observacao_admin or 'N/A'}

Com os melhores cumprimentos,
Direcção do Internato — IICB
    """

    _enviar_email(email_estudante, assunto, corpo)
    logger.info(
        f"[SINAL] Estudante {estudante.nome_completo} notificado — estado: {instance.estado}"
    )
