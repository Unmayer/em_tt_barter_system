from django.urls import path
from ads.views import create_advertisement, edit_advertisement, delete_advertisement, advertisement_list

urlpatterns = [
    path('', advertisement_list, name='ads_list'),
    path('ads/create/', create_advertisement, name='create_ad'),
    path('ads/<int:pk>/edit/', edit_advertisement, name='edit_ad'),
    path('ads/<int:pk>/delete/', delete_advertisement, name='delete_ad'),
]
