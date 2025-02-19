# Generated by Django 5.1.4 on 2025-02-19 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0006_userplancancelationreasons_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userplancancelationreasons',
            name='reason_ar',
            field=models.CharField(db_index=True, max_length=256, null=True, verbose_name='Reason'),
        ),
        migrations.AddField(
            model_name='userplancancelationreasons',
            name='reason_en',
            field=models.CharField(db_index=True, max_length=256, null=True, verbose_name='Reason'),
        ),
    ]
