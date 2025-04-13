import pytest
from django.urls import reverse

from ads.models import Ad, ExchangeProposal


@pytest.mark.django_db
class TestAd:
    def test_create_ad(self, test_user):
        ad = Ad.objects.create(
            user=test_user,
            title="ТестЗаголовок",
            description="ТестОписание",
            image_url='',
            category='ТестКатегория',
            condition=Ad.USED,
        )
        assert ad.title == "ТестЗаголовок"

    def test_edit_ad(self, client, test_user, test_ad):
        client.force_login(test_user)
        edit_data = {
            'title': 'Обновленный заголовок',
            'description': 'Новое описание',
            'category': 'books',
            'condition': 'used'
        }
        response = client.post(reverse('edit_ad', args=[test_ad.pk]), edit_data)
        assert response.status_code == 200
        test_ad.refresh_from_db()
        assert test_ad.title == 'Обновленный заголовок'

    def test_get_edit_form_owner(self, client, test_user, test_ad):
        client.force_login(test_user)
        response = client.get(reverse('edit_ad', args=[test_ad.pk]))
        assert response.status_code == 200
        assert 'form' in response.context

    def test_get_edit_form_non_owner(self, client, test_user, another_ad):
        client.force_login(test_user)
        response = client.get(reverse('edit_ad', args=[another_ad.pk]))
        assert response.status_code == 302

    def test_delete_ad(self, client, test_user, test_ad):
        client.force_login(test_user)
        response = client.post(reverse('delete_ad', args=[test_ad.pk]))
        assert response.status_code == 302
        assert not Ad.objects.filter(pk=test_ad.pk).exists()

    def test_search_ads(self, client, test_ad, another_ad):
        response = client.get(reverse('ads_list') + '?search=Test')
        assert response.status_code == 200
        assert test_ad in response.context['page_obj']
        assert another_ad not in response.context['page_obj']

    def test_filter_by_category(self, client, test_ad, another_ad):
        response = client.get(reverse('ads_list') + '?category=electronics')
        assert response.status_code == 200
        assert test_ad in response.context['page_obj']
        assert another_ad not in response.context['page_obj']

    def test_filter_by_condition(self, client, test_ad, another_ad):
        response = client.get(reverse('ads_list') + '?condition=new')
        assert response.status_code == 200
        assert test_ad in response.context['page_obj']
        assert another_ad not in response.context['page_obj']


@pytest.mark.django_db
class TestExchangeProposal:
    def test_create_proposal(self, test_ad, another_ad):
        proposal = ExchangeProposal.objects.create(
            ad_sender=test_ad,
            ad_receiver=another_ad,
            comment="Комментарий",
        )
        assert proposal.comment == "Комментарий"
        assert proposal.status == ExchangeProposal.AWAITING

    def test_change_status(self, test_user, client, test_proposal):
        client.force_login(test_user)
        edit_data = {
            'status': ExchangeProposal.ACCEPTED
        }
        response = client.post(reverse('edit_proposal', args=[test_proposal.pk]), edit_data)
        assert response.status_code == 302
        test_proposal.refresh_from_db()
        assert test_proposal.status == ExchangeProposal.ACCEPTED

    def test_filter_by_sender(self, client, test_proposal, another_proposal):
        response = client.get(reverse('proposals_list') + f'?ad_sender={test_proposal.ad_sender.title}')
        assert response.status_code == 200
        assert test_proposal in response.context['proposals']
        assert another_proposal not in response.context['proposals']

    def test_filter_by_receiver(self, client, test_proposal, another_proposal):
        response = client.get(reverse('proposals_list') + f'?ad_receiver={another_proposal.ad_receiver.title}')
        assert response.status_code == 200
        assert test_proposal not in response.context['proposals']
        assert another_proposal in response.context['proposals']

    def test_filter_by_status(self, client, test_proposal, another_proposal):
        response = client.get(reverse('proposals_list') + f'?status={another_proposal.status}')
        assert response.status_code == 200
        assert test_proposal not in response.context['proposals']
        assert another_proposal in response.context['proposals']
