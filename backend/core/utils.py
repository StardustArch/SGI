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