from payments.models import PaymentStatus, PaymentTransaction, PaymentEvent
from django.utils import timezone

# Define alllowed transitions of states

ALLOWED_TRANSITIONS = {
    PaymentStatus.CREATED: {PaymentStatus.PENDING},
    PaymentStatus.PENDING: {PaymentStatus.SUCCESS, PaymentStatus.FAILED}
    
}