# Generated by Django 4.2.16 on 2024-11-19 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='item_empresa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pedidos.empresa'),
        ),
    ]
