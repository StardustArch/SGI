from django.contrib.auth.backends import ModelBackend
from .models import Utilizador

class IdentificadorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username:
            return None
        # Tenta por código de acesso
        try:
            user = Utilizador.objects.get(codigo_acesso=username)
        except Utilizador.DoesNotExist:
            # Tenta por telefone
            try:
                user = Utilizador.objects.get(telefone=username)
            except Utilizador.DoesNotExist:
                # Tenta por email
                try:
                    user = Utilizador.objects.get(email=username)
                except Utilizador.DoesNotExist:
                    return None
        if user.check_password(password):
            return user
        return None