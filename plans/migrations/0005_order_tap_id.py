# Generated by Django 5.1.4 on 2025-02-18 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0004_plan_free_trial_days_userplan_activated_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tap_id',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Tap ID'),
        ),
    ]
