# Generated by Django 5.1.2 on 2024-10-27 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaVerde', '0003_carrito_carritoproducto_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Enviado', 'Enviado'), ('Cancelado', 'Cancelado')], default='Pendiente', max_length=20),
        ),
    ]
