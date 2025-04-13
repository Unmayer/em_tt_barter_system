import pytest
from django.contrib.auth.models import User

from ads.models import Ad, ExchangeProposal


@pytest.fixture
def client():
    from django.test import Client
    return Client()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username='otheruser',
        password='otherpass123'
    )


@pytest.fixture
def test_ad(test_user):
    return Ad.objects.create(
        title='Test Ad',
        description='Test Description',
        user=test_user,
        category='electronics',
        condition=Ad.NEW
    )


@pytest.fixture
def another_ad(another_user):
    return Ad.objects.create(
        title='Another Ad',
        description='Another Description',
        user=another_user,
        category='books',
        condition=Ad.USED
    )


@pytest.fixture
def test_proposal(test_ad, another_ad):
    return ExchangeProposal.objects.create(
        ad_sender=test_ad,
        ad_receiver=another_ad,
        comment="Первый",
    )


@pytest.fixture
def another_proposal(test_ad, another_ad):
    return ExchangeProposal.objects.create(
        ad_sender=another_ad,
        ad_receiver=test_ad,
        comment="Второй",
        status=ExchangeProposal.ACCEPTED,
    )
