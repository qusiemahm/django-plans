# Generated by Django 5.1.4 on 2025-02-19 08:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0005_order_tap_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPlanCancelationReasons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(db_index=True, max_length=256, verbose_name='Reason')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('hidden', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='userplan',
            name='cancelation_reason',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='plans.userplancancelationreasons', verbose_name='Cancelation Reason'),
        ),
    ]
