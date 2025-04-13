from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from ads.models import Ad, ExchangeProposal
from ads.forms import AdForm, AdSearchForm, ExchangeProposalForm, ExchangeProposalSearchForm
from ads.serializers import AdSerializer, ProposalSerializer


def advertisement_list(request):
    ads = Ad.objects.select_related('user').order_by('-created_at')
    form = AdSearchForm(request.GET or None)

    if form.is_valid():
        data = form.cleaned_data

        if data['search']:
            ads = ads.filter(
                Q(title__icontains=data['search']) |
                Q(description__icontains=data['search'])
            )

        if data['category']:
            ads = ads.filter(category__iexact=data['category'])

        if data['condition']:
            ads = ads.filter(condition=data['condition'])

    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ads_list.html', {
        'page_obj': page_obj,
        'form': form,
    })


@login_required
def create_advertisement(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return render(request, 'ads/confirmation.html', {'ad': ad, 'is_edit': False})
    else:
        form = AdForm()

    return render(request, 'ads/create_ad.html', {'form': form})


@login_required
def edit_advertisement(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if request.user != ad.user:
        messages.error(request, 'Вы не можете редактировать чужое объявление')
        return redirect('ads_list')

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return render(request, 'ads/confirmation.html', {'ad': ad, 'is_edit': True})
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/edit_ad.html', {'form': form})


@require_POST
@login_required()
def delete_advertisement(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    ad.delete()
    return redirect('ads_list')


@login_required
def create_exchange_proposal(request):
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.save()
            return redirect('proposals_list')
    else:
        form = ExchangeProposalForm(user=request.user)

    return render(request, 'ads/create_proposal.html', {
        'form': form,
    })


def proposal_list(request):
    proposals = (
        ExchangeProposal.objects.select_related('ad_sender', 'ad_receiver', 'ad_sender__user', 'ad_receiver__user')
        .order_by('-created_at')
    )
    form = ExchangeProposalSearchForm(request.GET or None)
    if form.is_valid():
        data = form.cleaned_data
        if data['ad_sender']:
            proposals = proposals.filter(ad_sender__title__icontains=data['ad_sender'])
        if data['ad_receiver']:
            proposals = proposals.filter(ad_receiver__title__icontains=data['ad_receiver'])
        if data['status']:
            proposals = proposals.filter(status=data['status'])

    return render(request, 'ads/proposals_list.html', {'proposals': proposals, 'form': form})


@login_required
def edit_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [ExchangeProposal.ACCEPTED, ExchangeProposal.REJECTED]:
            proposal.status = new_status
            proposal.save()
            messages.success(request, 'Статус обновлён')
            return redirect('proposals_list')
        else:
            messages.error(request, 'Некорректный статус')

    return render(request, 'ads/edit_proposal.html', {
        'proposal': proposal,
        'status_choices': ExchangeProposal.STATUS_CHOICES[1:]
    })


class AdListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ad.objects.select_related('user').order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProposalListCreateAPIView(generics.ListCreateAPIView):
    queryset = (
        ExchangeProposal.objects.select_related('ad_sender', 'ad_receiver', 'ad_sender__user', 'ad_receiver__user')
        .order_by('-created_at')
    )
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(status=ExchangeProposal.AWAITING)


class AdDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.select_related('user')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("У вас нет прав на редактирование этого объявления")
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class ProposalDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        ExchangeProposal.objects.select_related('ad_sender', 'ad_receiver', 'ad_sender__user', 'ad_receiver__user')
        .order_by('-created_at')
    )
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
