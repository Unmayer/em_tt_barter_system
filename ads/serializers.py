from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from ads.models import Ad, ExchangeProposal


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Пример создания объявления',
            value={
                'title': 'Название товара',
                'description': 'Описание товара',
                'category': 'electronics',
                'condition': 'new',
                'image_url': 'https://example.com/image.jpg'
            },
            request_only=True
        ),
        OpenApiExample(
            'Пример ответа',
            value={
                'id': 1,
                'title': 'Название товара',
                'description': 'Описание товара',
                'category': 'electronics',
                'condition': 'new',
                'image_url': 'https://example.com/image.jpg',
                'created_at': '2025-05-20T12:00:00Z',
                'user': 'username'
            },
            response_only=True
        )
    ]
)
class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    condition_display = serializers.CharField(source='get_condition_display', read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id',
            'title',
            'description',
            'category',
            'condition',
            'condition_display',
            'image_url',
            'created_at',
            'user'
        ]
        extra_kwargs = {
            'condition': {'write_only': True}
        }


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Пример создания предложения',
            value={
                'ad_sender_id': 1,
                'ad_receiver_id': 2,
                'comment': 'Предлагаю обмен',
                'status': 'awaiting'
            },
            request_only=True
        ),
        OpenApiExample(
            'Пример ответа',
            value={
                'id': 1,
                'ad_sender': {'id': 1, 'title': 'Мой товар'},
                'ad_receiver': {'id': 2, 'title': 'Чужой товар'},
                'comment': 'Предлагаю обмен',
                'status': 'awaiting',
                'created_at': '2025-05-20T12:00:00Z'
            },
            response_only=True
        )
    ]
)
class ProposalSerializer(serializers.ModelSerializer):
    ad_sender = AdSerializer(read_only=True)
    ad_receiver = AdSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    ad_sender_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        write_only=True,
        source='ad_sender',
        label="Объявление-инициатор",
    )
    ad_receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.all(),
        write_only=True,
        source='ad_receiver',
        label="Объявление-получатель",
    )

    class Meta:
        model = ExchangeProposal
        fields = [
            'id',
            'ad_sender',
            'ad_receiver',
            'ad_sender_id',
            'ad_receiver_id',
            'comment',
            'status',
            'status_display',
            'created_at'
        ]
        extra_kwargs = {
            'status': {'write_only': True}
        }
