# tests/unit/test_factories.py
import pytest
from tests.factories import (
    OrganisationFactory,
    SubscriptionFactory,
    OrganisationFactoryTier
)
from organisations.models import SubscriptionTier


@pytest.mark.django_db
class TestOrganisationFactory:
    def test_default_organisation_creation(self):
        org = OrganisationFactory()
        assert org.subscription_tier == SubscriptionTier.STARTER
        assert org.storage_limit == 10240
        assert org.owner is not None

    def test_tier_specific_organisation(self):
        pro_org = OrganisationFactoryTier.pro()
        assert pro_org.subscription_tier == SubscriptionTier.PRO
        assert pro_org.storage_limit == 51200
        assert pro_org.enable_scrum_hierarchy is True


@pytest.mark.django_db
class TestSubscriptionFactory:
    def test_default_subscription_creation(self):
        sub = SubscriptionFactory()
        assert sub.organisation is not None
        assert sub.current_user_count == 0
        assert sub.current_storage_used == 0

    def test_subscription_with_usage(self):
        sub = SubscriptionFactory.with_usage()

        # Check usage metrics are within limits
        assert 0 <= sub.current_storage_used <= sub.max_storage
        assert 1 <= sub.current_user_count <= sub.max_users
        assert 0 <= sub.current_item_count <= sub.max_items

    def test_subscription_with_specific_tier(self):
        org = OrganisationFactoryTier.enterprise()
        sub = SubscriptionFactory.with_usage(organisation=org)

        # Enterprise tier limits
        assert sub.current_user_count <= 999999  # Enterprise user limit
        assert sub.current_storage_used <= 1024000  # 1TB in MB
