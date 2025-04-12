from django import forms
from ads.models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class AdSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={'placeholder': 'По заголовку или описанию'})
    )
    category = forms.CharField(
        required=False,
        label='Категория',
        widget=forms.TextInput(attrs={'placeholder': 'Фильтр по категории'})
    )
    condition = forms.ChoiceField(
        choices=Ad.CONDITION_CHOICES,
        required=False,
        label='Состояние'
    )


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Ваше сообщение...',
                'rows': 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)
            self.fields['ad_receiver'].queryset = Ad.objects.exclude(user=user)


class ExchangeProposalSearchForm(forms.Form):
    ad_sender = forms.CharField(
        required=False,
        label='Инициатор',
        widget=forms.TextInput(attrs={'placeholder': 'Фильтр по инициатору'})
    )
    ad_receiver = forms.CharField(
        required=False,
        label='Получатель',
        widget=forms.TextInput(attrs={'placeholder': 'Фильтр по получателю'})
    )
    status = forms.ChoiceField(
        choices=ExchangeProposal.STATUS_CHOICES,
        required=False,
        label='Статус'
    )