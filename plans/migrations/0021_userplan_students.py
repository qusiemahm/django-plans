# Generated by Django 5.1.4 on 2025-01-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0020_plan_plan_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='userplan',
            name='students',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
