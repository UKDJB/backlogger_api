# organisations/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()


class BillingInterval(models.TextChoices):
    MONTHLY = 'MON', _('Monthly')
    ANNUAL = 'ANN', _('Annual')


class OrganisationStatus(models.TextChoices):
    ACTIVE = 'ACT', _('Active')
    SUSPENDED = 'SUS', _('Suspended')
    ARCHIVED = 'ARC', _('Archived')


class PaymentStatus(models.TextChoices):
    ACTIVE = 'ACT', _('Active')
    OVERDUE = 'OVR', _('Overdue')
    CANCELLED = 'CAN', _('Cancelled')


class ProjectFramework(models.TextChoices):
    KANBAN = 'KAN', _('Kanban')
    SCRUM = 'SCR', _('Scrum')
    WATERFALL = 'WAT', _('Waterfall')


class SubscriptionStatus(models.TextChoices):
    ACTIVE = 'ACT', _('Active')
    TRIALING = 'TRL', _('Trial Period')
    PAST_DUE = 'PDU', _('Past Due')
    CANCELLED = 'CAN', _('Cancelled')
    SUSPENDED = 'SUS', _('Suspended')


class SubscriptionTier(models.TextChoices):
    STARTER = 'STR', _('Starter')
    PRO = 'PRO', _('Pro')
    BUSINESS = 'BUS', _('Business')
    ENTERPRISE = 'ENT', _('Enterprise')


class Organisation(models.Model):
    """
    Core organisation model representing a client entity with all associated
    configuration, hierarchy settings, and subscription details.
    """
    # Core Identification
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=100,
        help_text=_("Organisation name")
    )

    # Status and Type
    status = models.CharField(
        max_length=3,
        choices=OrganisationStatus.choices,
        default=OrganisationStatus.ACTIVE
    )
    subscription_tier = models.CharField(
        max_length=3,
        choices=SubscriptionTier.choices,
        default=SubscriptionTier.STARTER
    )

    # Ownership and Access Control
    owner = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='owned_organisation',
        help_text=_("Admin owner of the organisation")
    )
    owner_email = models.EmailField(
        help_text=_("Email of the organisation owner")
    )
    allowed_domains = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of allowed email domains for Enterprise tier")
    )
    role_hierarchy = models.JSONField(
        default=dict,
        help_text=_("RBAC configuration for the organisation")
    )

    # Project and Hierarchy Configuration
    default_framework = models.CharField(
        max_length=3,
        choices=ProjectFramework.choices,
        default=ProjectFramework.KANBAN
    )
    enable_objective_layer = models.BooleanField(
        default=False,
        help_text=_("Enable Objective/Initiative hierarchy")
    )
    enable_platform_layer = models.BooleanField(
        default=False,
        help_text=_("Enable Platform/Application hierarchy")
    )
    enable_scrum_hierarchy = models.BooleanField(
        default=False,
        help_text=_("Enable Scrum-specific item types")
    )
    enable_waterfall = models.BooleanField(
        default=False,
        help_text=_("Enable Waterfall methodology")
    )

    # Billing and Subscription
    billing_contact = models.EmailField(
        blank=True,
        null=True,
        help_text=_("Billing contact email")
    )
    payment_status = models.CharField(
        max_length=3,
        choices=PaymentStatus.choices,
        default=PaymentStatus.ACTIVE
    )
    renewal_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Next subscription renewal date")
    )
    storage_limit = models.BigIntegerField(
        default=1024,  # 1GB in MB
        help_text=_("Storage quota in MB")
    )

    # Compliance and Logging
    gdpr_compliance = models.BooleanField(
        default=False,
        help_text=_("GDPR compliance enabled")
    )
    data_retention_policy = models.JSONField(
        default=dict,
        help_text=_("Data retention settings")
    )
    audit_logs = models.JSONField(
        default=list,
        help_text=_("Record of administrative actions")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['subscription_tier']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['owner_email'])
        ]

    def __str__(self):
        return f"{self.name} ({self.get_subscription_tier_display()})"

    def clean(self):
        """Validate organisation data and enforces business rules"""
        if self.subscription_tier != SubscriptionTier.ENTERPRISE and self.allowed_domains:
            raise ValidationError({
                'allowed_domains': _("Allowed domains are only available for Enterprise tier")
            })

        if not self.enable_scrum_hierarchy and self.default_framework == ProjectFramework.SCRUM:
            raise ValidationError({
                'default_framework': _("Cannot set Scrum as default when Scrum hierarchy is disabled")
            })

        if not self.enable_waterfall and self.default_framework == ProjectFramework.WATERFALL:
            raise ValidationError({
                'default_framework': _("Cannot set Waterfall as default when Waterfall is disabled")
            })

    def save(self, *args, **kwargs):
        # Set hierarchy enablement based on subscription tier
        if self.subscription_tier == SubscriptionTier.ENTERPRISE:
            self.enable_objective_layer = True
            self.enable_platform_layer = True
            self.enable_scrum_hierarchy = True
            self.enable_waterfall = True
            self.storage_limit = 1024000  # 1TB in MB
        elif self.subscription_tier == SubscriptionTier.BUSINESS:
            self.enable_objective_layer = True
            self.enable_platform_layer = True
            self.enable_scrum_hierarchy = True
            self.storage_limit = 102400   # 100GB in MB
        elif self.subscription_tier == SubscriptionTier.PRO:
            self.enable_scrum_hierarchy = True
            self.enable_platform_layer = False
            self.storage_limit = 51200    # 50GB in MB
        else:  # STARTER
            self.enable_objective_layer = False
            self.enable_platform_layer = False
            self.enable_scrum_hierarchy = False
            self.enable_waterfall = False
            self.storage_limit = 10240    # 10GB in MB

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_enterprise(self):
        """Check if organisation has Enterprise tier"""
        return self.subscription_tier == SubscriptionTier.ENTERPRISE


class Subscription(models.Model):
    """
    Tracks subscription details, billing, and usage for an organisation
    """
    # Core Fields
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    organisation = models.OneToOneField(
        'Organisation',
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    # Status and Billing
    status = models.CharField(
        max_length=3,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.TRIALING
    )
    billing_interval = models.CharField(
        max_length=3,
        choices=BillingInterval.choices,
        default=BillingInterval.MONTHLY
    )

    # Dates
    start_date = models.DateTimeField(
        help_text=_("When the subscription began")
    )
    current_period_start = models.DateTimeField(
        help_text=_("Start of current billing period")
    )
    current_period_end = models.DateTimeField(
        help_text=_("End of current billing period")
    )
    trial_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When trial period ends")
    )
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("When subscription was cancelled")
    )

    # Usage Tracking
    current_user_count = models.IntegerField(
        default=0,
        help_text=_("Current number of active users")
    )
    current_storage_used = models.BigIntegerField(
        default=0,
        help_text=_("Current storage used in MB")
    )
    current_item_count = models.IntegerField(
        default=0,
        help_text=_("Current number of items")
    )

    # Billing Details
    billing_email = models.EmailField(
        help_text=_("Email for billing communications")
    )
    billing_name = models.CharField(
        max_length=100,
        help_text=_("Name on billing account")
    )
    tax_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_("VAT or tax reference number")
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['current_period_end']),
            models.Index(fields=['trial_end']),
        ]

    def __str__(self):
        return f"{self.organisation.name} - {self.get_status_display()}"

    def clean(self):
        """Validate subscription data"""
        if self.current_period_end <= self.current_period_start:
            raise ValidationError({
                'current_period_end': _("Period end must be after period start")
            })

        if self.trial_end and self.trial_end <= self.start_date:
            raise ValidationError({
                'trial_end': _("Trial end must be after subscription start")
            })

        # Check usage against limits
        if self.current_user_count > self.max_users:
            raise ValidationError({
                'current_user_count': _("User count exceeds subscription limit")
            })

        if self.current_storage_used > self.max_storage:
            raise ValidationError({
                'current_storage_used': _("Storage usage exceeds subscription limit")
            })

        if self.current_item_count > self.max_items:
            raise ValidationError({
                'current_item_count': _("Item count exceeds subscription limit")
            })

    @property
    def max_users(self):
        """Maximum allowed users based on organisation tier"""
        tier_limits = {
            'STR': 10,     # Starter: 10 users
            'PRO': 50,     # Pro: 50 users
            'BUS': 250,    # Business: 250 users
            'ENT': 999999  # Enterprise: Unlimited
        }
        return tier_limits[self.organisation.subscription_tier]

    @property
    def max_storage(self):
        """Maximum allowed storage (MB) based on organisation tier"""
        return self.organisation.storage_limit

    @property
    def max_items(self):
        """Maximum allowed items based on organisation tier"""
        tier_limits = {
            'STR': 1000,   # Starter: 1,000 items
            'PRO': 10000,  # Pro: 10,000 items
            'BUS': 50000,  # Business: 50,000 items
            'ENT': 999999  # Enterprise: Unlimited
        }
        return tier_limits[self.organisation.subscription_tier]

    @property
    def is_trial(self):
        """Check if subscription is in trial period"""
        return self.status == SubscriptionStatus.TRIALING

    @property
    def is_active(self):
        """Check if subscription is active (including trial)"""
        return self.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]

    @property
    def is_cancelled(self):
        """Check if subscription has been cancelled"""
        return self.status == SubscriptionStatus.CANCELLED
