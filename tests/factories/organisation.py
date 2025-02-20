# tests/factories/organisation.py
"""Test factories for Organisation and Subscription models."""
import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from organisations.models import (
    Organisation,
    Subscription,
    OrganisationStatus,
    SubscriptionStatus,
    SubscriptionTier,
    BillingInterval,
    PaymentStatus
)
from tests.factories import UserFactory


class OrganisationFactory(DjangoModelFactory):
    """Factory for generating test organisations."""

    class Meta:
        model = Organisation

    # Core Fields
    name = factory.Sequence(lambda n: f'Test Organisation {n}')
    status = OrganisationStatus.ACTIVE
    subscription_tier = SubscriptionTier.STARTER

    # Owner and Access Control
    owner = factory.SubFactory(UserFactory)
    owner_email = factory.LazyAttribute(lambda o: o.owner.email)
    allowed_domains = factory.List([])

    # Add default JSON fields
    role_hierarchy = factory.Dict({
        'admin': ['write', 'read'],
        'user': ['read']
    })
    data_retention_policy = factory.Dict({
        'audit_logs_days': 30,
        'user_data_years': 7
    })
    audit_logs = factory.List([{
        'timestamp': timezone.now().isoformat(),
        'action': 'created',
        'actor': 'system',
        'details': 'Organisation created'
    }])

    # Project Configuration
    default_framework = 'KAN'
    enable_objective_layer = False
    enable_platform_layer = False
    enable_scrum_hierarchy = False
    enable_waterfall = False

    # Billing
    payment_status = PaymentStatus.ACTIVE
    storage_limit = 1024  # 1GB default

    # Compliance
    gdpr_compliance = False

# Tier-specific factory traits


class OrganisationFactoryTier:
    """Traits for different organisation tiers."""

    @staticmethod
    def starter():
        return OrganisationFactory(subscription_tier=SubscriptionTier.STARTER)

    @staticmethod
    def pro():
        return OrganisationFactory(
            subscription_tier=SubscriptionTier.PRO,
            enable_scrum_hierarchy=True,
            storage_limit=51200
        )

    @staticmethod
    def business():
        return OrganisationFactory(
            subscription_tier=SubscriptionTier.BUSINESS,
            enable_objective_layer=True,
            enable_platform_layer=True,
            enable_scrum_hierarchy=True,
            storage_limit=102400
        )

    @staticmethod
    def enterprise():
        return OrganisationFactory(
            subscription_tier=SubscriptionTier.ENTERPRISE,
            enable_objective_layer=True,
            enable_platform_layer=True,
            enable_scrum_hierarchy=True,
            enable_waterfall=True,
            storage_limit=1024000,
            allowed_domains=['example.com']
        )


class SubscriptionFactory(DjangoModelFactory):
    """Factory for generating test subscriptions."""

    class Meta:
        model = Subscription

    # Core Fields
    organisation = factory.SubFactory(OrganisationFactory)
    status = SubscriptionStatus.ACTIVE
    billing_interval = BillingInterval.MONTHLY

    # Dates
    start_date = factory.LazyFunction(timezone.now)
    current_period_start = factory.LazyFunction(timezone.now)
    current_period_end = factory.LazyAttribute(
        lambda o: o.current_period_start + timezone.timedelta(days=30)
    )
    trial_end = None
    cancelled_at = None

    # Usage
    current_user_count = 0
    current_storage_used = 0
    current_item_count = 0

    # Billing Details
    billing_email = factory.LazyAttribute(lambda o: o.organisation.owner_email)
    billing_name = factory.LazyAttribute(lambda o: o.organisation.name)
    tax_number = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to ensure subscription matches organisation tier."""
        subscription = super()._create(model_class, *args, **kwargs)
        # Update organisation's renewal date
        subscription.organisation.renewal_date = subscription.current_period_end
        subscription.organisation.save()
        return subscription

    @classmethod
    def with_usage(cls, **kwargs):
        """Create subscription with realistic usage metrics."""
        subscription = cls.create(**kwargs)
        metrics = UsageMetricsGenerator()

        subscription.current_storage_used = metrics.generate_storage_metrics(
            subscription.max_storage
        )
        subscription.current_user_count = metrics.generate_user_metrics(
            subscription.max_users
        )
        subscription.current_item_count = metrics.generate_item_metrics(
            subscription.max_items
        )
        subscription.save()

        return subscription


class UsageMetricsGenerator:
    """Generator for realistic subscription usage metrics."""

    @staticmethod
    def generate_storage_metrics(max_limit):
        """Generate realistic storage usage within limit."""
        fake = factory.Faker._get_faker()
        return fake.random_int(min=0, max=max_limit)

    @staticmethod
    def generate_user_metrics(max_users):
        """Generate realistic user counts within subscription limit."""
        fake = factory.Faker._get_faker()
        return fake.random_int(min=1, max=max_users)

    @staticmethod
    def generate_item_metrics(max_items):
        """Generate realistic item counts within subscription limit."""
        fake = factory.Faker._get_faker()
        return fake.random_int(min=0, max=max_items)
