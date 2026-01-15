from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from payments.serializers import PaymentInitiateSerializer
from payments.models import PaymentTransaction
from payments.services.mpesa import initiate_mpesa_payment
from payments.services.paystack import initiate_paystack_payment

class PaymentInitiateView(APIView):
    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        transaction = PaymentTransaction.objects.create(
            provider=data["provider"],
            amount=data["amount"],
            currency=data["currency"],
        )

        if data["provider"] == "mpesa":
            response = initiate_mpesa_payment(
                transaction,
                phone_number=data.get("phone_number")
            )
        
        elif data["provider"] == "paystack":
            response = initiate_paystack_payment(
                transaction,
                email=data.get("email"),
            )

        return Response(
            {
                "status":"pending",
                "refrence": transaction.reference,
                "provider_response": response,
            }
        )