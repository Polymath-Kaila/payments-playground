from rest_framework import serializers
from payments.models import PaymentProvider

class PaymentInitiateSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=PaymentProvider.choices)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(default="KES")
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    