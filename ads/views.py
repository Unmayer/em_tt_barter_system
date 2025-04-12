from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from ads.models import Ad
from ads.forms import AdForm, AdSearchForm


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
        return HttpResponseForbidden()

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
