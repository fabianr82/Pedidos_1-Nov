# Generated by Django 4.2.16 on 2024-11-05 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0005_producto_item_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='item_empresa',
            field=models.CharField(blank=True, default=1, max_length=10, null=True),
        ),
    ]
