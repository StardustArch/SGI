from django.db import migrations

def popular_perfis_iniciais(apps, schema_editor):
    Perfil = apps.get_model('core', 'Perfil')
    Perfil.objects.create(nome_perfil='Administrador', descricao='Acesso total.')
    Perfil.objects.create(nome_perfil='Estudante', descricao='Acesso de consulta.')
    Perfil.objects.create(nome_perfil='Encarregado', descricao='Acesso de consulta.')

def reverter_perfis(apps, schema_editor):
    Perfil = apps.get_model('core', 'Perfil')
    Perfil.objects.filter(nome_perfil__in=['Administrador', 'Estudante', 'Encarregado']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'), 
    ]
    operations = [
        migrations.RunPython(popular_perfis_iniciais, reverter_perfis),
    ]