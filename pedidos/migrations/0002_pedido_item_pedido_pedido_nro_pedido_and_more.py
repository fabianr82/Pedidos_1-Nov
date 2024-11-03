# Generated by Django 4.2.16 on 2024-11-03 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='item_pedido',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='pedido',
            name='nro_pedido',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name='pedido',
            unique_together={('nro_pedido', 'item_pedido')},
        ),
    ]
