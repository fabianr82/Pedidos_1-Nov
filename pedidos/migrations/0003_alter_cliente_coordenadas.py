# Generated by Django 5.1.5 on 2025-01-28 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_alter_pedido_estatusped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='coordenadas',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
