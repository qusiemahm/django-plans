# Generated by Django 5.1.4 on 2024-12-26 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0015_alter_billinginfo_id_alter_invoice_id_alter_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='planpricing',
            name='regular_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]