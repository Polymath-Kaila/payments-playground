from django.urls import path
from payments.views import PaymentInitiateView

urlpatterns = [
    path("/payments/initiate/", PaymentIniateView.as_view()),
]