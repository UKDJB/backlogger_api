# Generated by Django 5.1.6 on 2025-02-18 17:18

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Organisation name', max_length=100)),
                ('status', models.CharField(choices=[('ACT', 'Active'), ('SUS', 'Suspended'), ('ARC', 'Archived')], default='ACT', max_length=3)),
                ('subscription_tier', models.CharField(choices=[('STR', 'Starter'), ('PRO', 'Pro'), ('BUS', 'Business'), ('ENT', 'Enterprise')], default='STR', max_length=3)),
                ('owner_email', models.EmailField(help_text='Email of the organisation owner', max_length=254)),
                ('allowed_domains', models.JSONField(blank=True, default=list, help_text='List of allowed email domains for Enterprise tier')),
                ('role_hierarchy', models.JSONField(default=dict, help_text='RBAC configuration for the organisation')),
                ('default_framework', models.CharField(choices=[('KAN', 'Kanban'), ('SCR', 'Scrum'), ('WAT', 'Waterfall')], default='KAN', max_length=3)),
                ('enable_objective_layer', models.BooleanField(default=False, help_text='Enable Objective/Initiative hierarchy')),
                ('enable_platform_layer', models.BooleanField(default=False, help_text='Enable Platform/Application hierarchy')),
                ('enable_scrum_hierarchy', models.BooleanField(default=False, help_text='Enable Scrum-specific item types')),
                ('enable_waterfall', models.BooleanField(default=False, help_text='Enable Waterfall methodology')),
                ('billing_contact', models.EmailField(blank=True, help_text='Billing contact email', max_length=254, null=True)),
                ('payment_status', models.CharField(choices=[('ACT', 'Active'), ('OVR', 'Overdue'), ('CAN', 'Cancelled')], default='ACT', max_length=3)),
                ('renewal_date', models.DateTimeField(blank=True, help_text='Next subscription renewal date', null=True)),
                ('storage_limit', models.BigIntegerField(default=1024, help_text='Storage quota in MB')),
                ('gdpr_compliance', models.BooleanField(default=False, help_text='GDPR compliance enabled')),
                ('data_retention_policy', models.JSONField(default=dict, help_text='Data retention settings')),
                ('audit_logs', models.JSONField(default=list, help_text='Record of administrative actions')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.OneToOneField(help_text='Admin owner of the organisation', on_delete=django.db.models.deletion.PROTECT, related_name='owned_organisation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('ACT', 'Active'), ('TRL', 'Trial Period'), ('PDU', 'Past Due'), ('CAN', 'Cancelled'), ('SUS', 'Suspended')], default='TRL', max_length=3)),
                ('billing_interval', models.CharField(choices=[('MON', 'Monthly'), ('ANN', 'Annual')], default='MON', max_length=3)),
                ('start_date', models.DateTimeField(help_text='When the subscription began')),
                ('current_period_start', models.DateTimeField(help_text='Start of current billing period')),
                ('current_period_end', models.DateTimeField(help_text='End of current billing period')),
                ('trial_end', models.DateTimeField(blank=True, help_text='When trial period ends', null=True)),
                ('cancelled_at', models.DateTimeField(blank=True, help_text='When subscription was cancelled', null=True)),
                ('current_user_count', models.IntegerField(default=0, help_text='Current number of active users')),
                ('current_storage_used', models.BigIntegerField(default=0, help_text='Current storage used in MB')),
                ('current_item_count', models.IntegerField(default=0, help_text='Current number of items')),
                ('billing_email', models.EmailField(help_text='Email for billing communications', max_length=254)),
                ('billing_name', models.CharField(help_text='Name on billing account', max_length=100)),
                ('tax_number', models.CharField(blank=True, help_text='VAT or tax reference number', max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organisation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='organisations.organisation')),
            ],
        ),
        migrations.AddIndex(
            model_name='organisation',
            index=models.Index(fields=['subscription_tier'], name='organisatio_subscri_24019d_idx'),
        ),
        migrations.AddIndex(
            model_name='organisation',
            index=models.Index(fields=['status'], name='organisatio_status_d2bac9_idx'),
        ),
        migrations.AddIndex(
            model_name='organisation',
            index=models.Index(fields=['payment_status'], name='organisatio_payment_3afb2e_idx'),
        ),
        migrations.AddIndex(
            model_name='organisation',
            index=models.Index(fields=['owner_email'], name='organisatio_owner_e_e00fe6_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['status'], name='organisatio_status_72f326_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['current_period_end'], name='organisatio_current_0e1905_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['trial_end'], name='organisatio_trial_e_8ce79a_idx'),
        ),
    ]
