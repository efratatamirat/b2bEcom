# Generated by Django 5.0.3 on 2024-04-27 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_order_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]