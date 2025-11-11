# Ficheiro: backend/core/management/commands/enviar_lembretes.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from core.models import Mensalidade
import datetime

class Command(BaseCommand):
    """
    Comando de gestão para enviar lembretes de pagamento.
    Executado por um Cron Job (agendador).
    """
    help = 'Envia emails de lembrete para mensalidades pendentes que vencem em 5 dias.'

    def handle(self, *args, **options):
        
        # --- Lógica de Vencimento (Ajustável) ---
        # 1. Queremos avisar sobre pagamentos 5 dias ANTES do vencimento.
        # Vamos assumir que a data de vencimento é todo dia 10 do mês.
        
        hoje = timezone.now().date()
        
        # Se hoje for dia 5 (10 - 5 = 5), procuramos pagamentos
        # deste mês que ainda estejam pendentes.
        DIA_DE_AVISO = 5 # Avisar no dia 5 de cada mês
        
        if hoje.day != DIA_DE_AVISO:
            self.stdout.write(f"Hoje não é dia {DIA_DE_AVISO}. Nenhum lembrete enviado.")
            return

        # 2. Encontrar o mês de referência actual
        primeiro_dia_mes = hoje.replace(day=1)

        # 3. Encontrar as mensalidades-alvo
        mensalidades_pendentes = Mensalidade.objects.filter(
            mes_referencia=primeiro_dia_mes,
            estado='Pendente'
        )

        self.stdout.write(f"--- A verificar pagamentos pendentes para {primeiro_dia_mes.strftime('%B de %Y')} ---")

        if not mensalidades_pendentes.exists():
            self.stdout.write("Nenhuma mensalidade pendente encontrada para este mês.")
            return

        total_enviados = 0
        
        # 4. Enviar os emails
        for mensalidade in mensalidades_pendentes:
            estudante = mensalidade.estudante
            encarregado = estudante.encarregado
            
            subject = f"Lembrete de Pagamento (SGI): {estudante.nome_completo}"
            message_body = f"""
            Exmo(a). Sr(a). {encarregado.nome_completo},
            
            Este é um lembrete amigável de que a mensalidade do internato
            para o seu educando, {estudante.nome_completo}, referente ao
            mês de {mensalidade.mes_referencia.strftime('%B de %Y')},
            ainda se encontra pendente.
            
            Por favor, efectue o pagamento até ao dia 10 para evitar constrangimentos.
            
            Com os melhores cumprimentos,
            A Direcção do Internato IICB
            """
            
            try:
                send_mail(
                    subject,
                    message_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [encarregado.email_contacto],
                    fail_silently=False,
                )
                self.stdout.write(f"Lembrete enviado para {encarregado.email_contacto}")
                total_enviados += 1
            except Exception as e:
                self.stderr.write(f"ERRO ao enviar para {encarregado.email_contacto}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"--- Concluído. Total de {total_enviados} lembretes enviados. ---"))