# signals.py

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group

def crear_grupos(sender, **kwargs):
    roles = ['Cliente', 'Vendedor']
    for rol in roles:
        Group.objects.get_or_create(name=rol)

class TuAplicacionConfig(AppConfig):
    name = 'tiendaVerde'  

    def ready(self):
        post_migrate.connect(crear_grupos, sender=self)
