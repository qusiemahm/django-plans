# Generated by Django 5.1.4 on 2025-01-15 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0019_alter_planpricing_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='plan_for',
            field=models.CharField(choices=[('vendors', 'vendors'), ('schools', 'schools')], default='vendors', max_length=20, verbose_name='Plan for'),
        ),
    ]
