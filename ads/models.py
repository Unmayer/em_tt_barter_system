from django.conf import settings
from django.db import models


class CreatedDateMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class Ad(CreatedDateMixin, models.Model):
    NEW = 'new'
    USED = 'used'
    REFURBISHED = 'refurbished'

    CONDITION_CHOICES = [
        (NEW, 'Новый'),
        (USED, 'Б/у'),
        (REFURBISHED, 'Восстановленный'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name='Автор объявления',
    )
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    description = models.CharField(max_length=2048, verbose_name='Описание')
    image_url = models.URLField(max_length=256, blank=True, null=True, verbose_name='URL изображения')
    category = models.CharField(max_length=128, verbose_name='Категория')
    condition = models.CharField(max_length=25, choices=CONDITION_CHOICES, verbose_name='Состояние')

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.title


class ExchangeProposal(CreatedDateMixin, models.Model):
    AWAITING = 'awaiting'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (AWAITING, 'Ожидает'),
        (ACCEPTED, 'Принята'),
        (REJECTED, 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='proposals_as_sender',
        verbose_name='Объявление-инициатор',
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='proposals_as_receiver',
        verbose_name='Объявление-получатель',
    )
    comment = models.CharField(max_length=2048, verbose_name='Комментарий')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=AWAITING, verbose_name='Статус')

    class Meta:
        verbose_name = "Предложение об обмене"
        verbose_name_plural = "Предложения об обмене"

    def __str__(self):
        return f'Сделка №{self.id}'




