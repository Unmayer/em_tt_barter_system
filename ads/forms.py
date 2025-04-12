from django import forms
from ads.models import Ad


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
