# Ficheiro: backend/core/utils.py

from django.utils import timezone


def gerar_numero_recibo() -> str:
    """
    Gera um número de recibo único no formato REC-YYYY-NNNN.
    Importado pela view GerarReciboView.
    Não está no modelo para evitar imports circulares.
    """
    from .models import Mensalidade

    ano = timezone.now().year
    ultimo = (
        Mensalidade.objects
        .filter(numero_recibo__startswith=f"REC-{ano}-")
        .order_by('-numero_recibo')
        .first()
    )

    if ultimo and ultimo.numero_recibo:
        try:
            num = int(ultimo.numero_recibo.split('-')[-1]) + 1
        except (ValueError, IndexError):
            num = 1
    else:
        num = 1

    return f"REC-{ano}-{num:04d}"