# Generated by Django 5.1.5 on 2025-02-04 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='user',
        ),
        migrations.AddField(
            model_name='pedido',
            name='forma_entrega',
            field=models.CharField(choices=[('domicilio', 'A domicilio'), ('retirar', 'Retirar en la empresa')], default='retirar', max_length=20),
        ),
    ]
