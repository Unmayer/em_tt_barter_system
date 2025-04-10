from django.contrib import admin
from ads.models import Ad, ExchangeProposal


@admin.register(Ad)
class AdvertisementAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(ExchangeProposal)
