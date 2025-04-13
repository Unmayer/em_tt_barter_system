from django.urls import path
from ads.views import (
    create_advertisement,
    edit_advertisement,
    delete_advertisement,
    advertisement_list,
    create_exchange_proposal,
    proposal_list,
    edit_proposal,
    AdListCreateAPIView,
    ProposalListCreateAPIView,
    AdDetailAPIView,
    ProposalDetailAPIView,
)

urlpatterns = [
    path('ads/<int:pk>/edit/', edit_advertisement, name='edit_ad'),
    path('ads/<int:pk>/delete/', delete_advertisement, name='delete_ad'),
    path('ads/create/', create_advertisement, name='create_ad'),
    path('', advertisement_list, name='ads_list'),

    path('proposals/edit/<int:proposal_id>/', edit_proposal, name='edit_proposal'),
    path('proposal/create/', create_exchange_proposal, name='create_proposal'),
    path('proposals/', proposal_list, name='proposals_list'),

    path('api/ads/<int:pk>/', AdDetailAPIView.as_view(), name='ad-detail'),
    path('api/ads/', AdListCreateAPIView.as_view(), name='api-ads'),

    path('api/proposals/<int:pk>/', ProposalDetailAPIView.as_view(), name='proposal-detail'),
    path('api/proposals/', ProposalListCreateAPIView.as_view(), name='api-proposals'),
]
