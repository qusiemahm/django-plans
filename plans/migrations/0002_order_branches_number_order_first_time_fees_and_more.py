# Generated by Django 5.1.4 on 2025-02-10 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='branches_number',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=4, null=True, verbose_name='Branches Number'),
        ),
        migrations.AddField(
            model_name='order',
            name='first_time_fees',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=4, null=True, verbose_name='First time fees'),
        ),
        migrations.AddField(
            model_name='order',
            name='students_fees',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=4, null=True, verbose_name='Students fees'),
        ),
    ]
