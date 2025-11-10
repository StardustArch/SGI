from django.contrib import admin

# Register your models here.
from .models import (
    Utilizador,
    Perfil,
    Encarregado,
    Estudante,
    Mensalidade,
    PresencaEstudo,
    Sancao,
    PedidoSaida
)

admin.site.register(Utilizador)
admin.site.register(Perfil)
admin.site.register(Encarregado)
admin.site.register(Estudante)
admin.site.register(Mensalidade)
admin.site.register(PresencaEstudo)
admin.site.register(Sancao)
admin.site.register(PedidoSaida)