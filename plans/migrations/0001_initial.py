# Generated by Django 5.1.4 on 2025-01-23 15:25

import django.core.validators
import django.db.models.deletion
import django_countries.fields
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='name')),
                ('name_ar', models.CharField(max_length=100, null=True, verbose_name='name')),
                ('period', models.PositiveIntegerField(blank=True, db_index=True, default=30, null=True, verbose_name='period')),
                ('url', models.URLField(blank=True, help_text='Optional link to page with more information (for clickable pricing table headers)')),
            ],
            options={
                'verbose_name': 'Pricing',
                'verbose_name_plural': 'Pricings',
                'ordering': ('period',),
                'abstract': False,
                'swappable': 'PLANS_PRICING_MODEL',
            },
        ),
        migrations.CreateModel(
            name='Quota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('codename', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='codename')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='name')),
                ('name_ar', models.CharField(max_length=100, null=True, verbose_name='name')),
                ('unit', models.CharField(blank=True, max_length=100, verbose_name='unit')),
                ('unit_en', models.CharField(blank=True, max_length=100, null=True, verbose_name='unit')),
                ('unit_ar', models.CharField(blank=True, max_length=100, null=True, verbose_name='unit')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_ar', models.TextField(blank=True, null=True, verbose_name='description')),
                ('is_boolean', models.BooleanField(default=False, verbose_name='is boolean')),
                ('url', models.CharField(blank=True, help_text='Optional link to page with more information (for clickable pricing table headers)', max_length=200)),
            ],
            options={
                'verbose_name': 'Quota',
                'verbose_name_plural': 'Quotas',
                'ordering': ('order',),
                'abstract': False,
                'swappable': 'PLANS_QUOTA_MODEL',
            },
        ),
        migrations.CreateModel(
            name='BillingInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('tax_number', models.CharField(blank=True, db_index=True, max_length=200, verbose_name='VAT ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='name')),
                ('street', models.CharField(max_length=200, verbose_name='street')),
                ('zipcode', models.CharField(max_length=200, verbose_name='zip code')),
                ('city', models.CharField(max_length=200, verbose_name='city')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='country')),
                ('shipping_name', models.CharField(blank=True, help_text='optional', max_length=200, verbose_name='name (shipping)')),
                ('shipping_street', models.CharField(blank=True, help_text='optional', max_length=200, verbose_name='street (shipping)')),
                ('shipping_zipcode', models.CharField(blank=True, help_text='optional', max_length=200, verbose_name='zip code (shipping)')),
                ('shipping_city', models.CharField(blank=True, help_text='optional', max_length=200, verbose_name='city (shipping)')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Billing info',
                'verbose_name_plural': 'Billing infos',
                'abstract': False,
                'swappable': 'PLANS_BILLINGINFO_MODEL',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('flat_name', models.CharField(blank=True, max_length=200, null=True)),
                ('completed', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='completed')),
                ('plan_extended_from', models.DateField(blank=True, help_text='The plan was extended from this date', null=True, verbose_name='plan extended from')),
                ('plan_extended_until', models.DateField(blank=True, help_text='The plan was extended until this date', null=True, verbose_name='plan extended until')),
                ('amount', models.DecimalField(db_index=True, decimal_places=2, max_digits=7, verbose_name='amount')),
                ('tax', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=4, null=True, verbose_name='tax')),
                ('currency', models.CharField(default='EUR', max_length=3, verbose_name='currency')),
                ('status', models.IntegerField(choices=[(1, 'new'), (2, 'completed'), (3, 'not valid'), (4, 'canceled'), (5, 'returned')], default=1, verbose_name='status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('-created',),
                'abstract': False,
                'swappable': 'PLANS_ORDER_MODEL',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('number', models.IntegerField(db_index=True)),
                ('full_number', models.CharField(max_length=200)),
                ('type', models.IntegerField(choices=[(1, 'Invoice'), (2, 'Invoice Duplicate'), (3, 'Order confirmation')], db_index=True, default=1)),
                ('issued', models.DateField(db_index=True)),
                ('issued_duplicate', models.DateField(blank=True, db_index=True, null=True)),
                ('selling_date', models.DateField(blank=True, db_index=True, null=True)),
                ('payment_date', models.DateField(db_index=True)),
                ('unit_price_net', models.DecimalField(decimal_places=2, max_digits=7)),
                ('quantity', models.IntegerField(default=1)),
                ('total_net', models.DecimalField(decimal_places=2, max_digits=7)),
                ('total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('tax_total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('tax', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=4, null=True)),
                ('rebate', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=4)),
                ('currency', models.CharField(default='EUR', max_length=3)),
                ('item_description', models.CharField(max_length=200)),
                ('buyer_name', models.CharField(blank=True, max_length=200, verbose_name='Name')),
                ('buyer_street', models.CharField(blank=True, max_length=200, verbose_name='Street')),
                ('buyer_zipcode', models.CharField(blank=True, max_length=200, verbose_name='Zip code')),
                ('buyer_city', models.CharField(blank=True, max_length=200, verbose_name='City')),
                ('buyer_country', django_countries.fields.CountryField(blank=True, default='PL', max_length=2, verbose_name='Country')),
                ('buyer_tax_number', models.CharField(blank=True, max_length=200, verbose_name='TAX/VAT number')),
                ('shipping_name', models.CharField(blank=True, max_length=200, verbose_name='Name')),
                ('shipping_street', models.CharField(blank=True, max_length=200, verbose_name='Street')),
                ('shipping_zipcode', models.CharField(blank=True, max_length=200, verbose_name='Zip code')),
                ('shipping_city', models.CharField(blank=True, max_length=200, verbose_name='City')),
                ('shipping_country', django_countries.fields.CountryField(blank=True, default='PL', max_length=2, verbose_name='Country')),
                ('require_shipment', models.BooleanField(db_index=True, default=False)),
                ('issuer_name', models.CharField(max_length=200, verbose_name='Name')),
                ('issuer_street', models.CharField(max_length=200, verbose_name='Street')),
                ('issuer_zipcode', models.CharField(max_length=200, verbose_name='Zip code')),
                ('issuer_city', models.CharField(max_length=200, verbose_name='City')),
                ('issuer_country', django_countries.fields.CountryField(default='PL', max_length=2, verbose_name='Country')),
                ('issuer_tax_number', models.CharField(blank=True, max_length=200, verbose_name='TAX/VAT number')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.PLANS_ORDER_MODEL, verbose_name='order')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'abstract': False,
                'swappable': 'PLANS_INVOICE_MODEL',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('name_en', models.CharField(max_length=100, null=True, verbose_name='name')),
                ('name_ar', models.CharField(max_length=100, null=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_ar', models.TextField(blank=True, null=True, verbose_name='description')),
                ('default', models.BooleanField(db_index=True, default=None, help_text='Both "Unknown" and "No" means that the plan is not default', null=True, unique=True)),
                ('available', models.BooleanField(db_index=True, default=False, help_text='Is still available for purchase', verbose_name='available')),
                ('visible', models.BooleanField(db_index=True, default=True, help_text='Is visible in current offer', verbose_name='visible')),
                ('url', models.URLField(blank=True, help_text='Optional link to page with more information (for clickable pricing table headers)')),
                ('plan_for', models.CharField(choices=[('vendors', 'vendors'), ('schools', 'schools')], default='vendors', max_length=20, verbose_name='Plan for')),
                ('price_per_student', models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=7, validators=[django.core.validators.MinValueValidator(0)])),
                ('customized', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='customized')),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Plans',
                'ordering': ('order',),
                'abstract': False,
                'swappable': 'PLANS_PLAN_MODEL',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_order', to=settings.PLANS_PLAN_MODEL, verbose_name='plan'),
        ),
        migrations.CreateModel(
            name='PlanPricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(1)])),
                ('regular_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('order', models.IntegerField(default=0)),
                ('has_automatic_renewal', models.BooleanField(default=False, help_text='Use automatic renewal if possible?', verbose_name='has automatic renewal')),
                ('visible', models.BooleanField(default=True, help_text='Is visible in current offer', verbose_name='is visible by default')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.PLANS_PLAN_MODEL)),
                ('pricing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.PLANS_PRICING_MODEL)),
            ],
            options={
                'verbose_name': 'Plan pricing',
                'verbose_name_plural': 'Plans pricings',
                'ordering': ('order', 'pricing__period'),
                'abstract': False,
                'swappable': 'PLANS_PLANPRICING_MODEL',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='pricing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.PLANS_PRICING_MODEL, verbose_name='pricing'),
        ),
        migrations.CreateModel(
            name='PlanQuota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('value', models.BigIntegerField(blank=True, default=1, null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.PLANS_PLAN_MODEL)),
                ('quota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.PLANS_QUOTA_MODEL)),
            ],
            options={
                'verbose_name': 'Plan quota',
                'verbose_name_plural': 'Plans quotas',
                'abstract': False,
                'swappable': 'PLANS_PLANQUOTA_MODEL',
            },
        ),
        migrations.AddField(
            model_name='plan',
            name='quotas',
            field=models.ManyToManyField(through='plans.PlanQuota', to=settings.PLANS_QUOTA_MODEL),
        ),
        migrations.CreateModel(
            name='UserPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('expire', models.DateField(blank=True, db_index=True, default=None, null=True, verbose_name='expire')),
                ('branches', models.PositiveIntegerField(default=1)),
                ('students', models.PositiveIntegerField(default=1)),
                ('active', models.BooleanField(db_index=True, default=True, verbose_name='active')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.PLANS_PLAN_MODEL, verbose_name='plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'User plan',
                'verbose_name_plural': 'Users plans',
                'abstract': False,
                'swappable': 'PLANS_USERPLAN_MODEL',
            },
        ),
        migrations.CreateModel(
            name='RecurringUserPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('token', models.CharField(blank=True, default=None, help_text='Token, that will be used for payment renewal. Depends on used payment provider', max_length=255, null=True, verbose_name='recurring token')),
                ('payment_provider', models.CharField(blank=True, default=None, help_text='Provider, that will be used for payment renewal', max_length=255, null=True, verbose_name='payment provider')),
                ('amount', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=7, null=True, verbose_name='amount')),
                ('tax', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=4, null=True, verbose_name='tax')),
                ('currency', models.CharField(max_length=3, verbose_name='currency')),
                ('renewal_triggered_by', models.IntegerField(choices=[(1, 'other'), (2, 'user'), (3, 'task')], db_index=True, default=2, help_text="The source of the associated plan's renewal (USER = user-initiated renewal, TASK = autorenew_account-task-initiated renewal, OTHER = renewal is triggered using another mechanism).", verbose_name='renewal triggered by')),
                ('_has_automatic_renewal_backup_deprecated', models.BooleanField(db_column='has_automatic_renewal', default=False, help_text='Automatic renewal is enabled for associated plan. If False, the plan renewal can be still initiated by user.', verbose_name='has automatic plan renewal')),
                ('token_verified', models.BooleanField(default=False, help_text='The recurring token has been verified by at least one payment to be working.', verbose_name='token has been verified by payment')),
                ('card_expire_year', models.IntegerField(blank=True, null=True)),
                ('card_expire_month', models.IntegerField(blank=True, null=True)),
                ('card_masked_number', models.CharField(blank=True, max_length=255, null=True)),
                ('pricing', models.ForeignKey(blank=True, default=None, help_text='Recurring pricing', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.PLANS_PRICING_MODEL)),
                ('user_plan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recurring', to=settings.PLANS_USERPLAN_MODEL)),
            ],
            options={
                'abstract': False,
                'swappable': 'PLANS_RECURRINGUSERPLAN_MODEL',
            },
        ),
    ]
