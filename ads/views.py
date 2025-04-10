from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from ads.models import Ad
from ads.forms import AdForm


def advertisement_list(request):
    ads = Ad.objects.all()
    return render(request, 'ads/ads_list.html', {'ads': ads})


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
    if request.method == 'POST':
        ad.delete()
        messages.success(request, "Заказ удалён")
        return redirect('ads_list')
