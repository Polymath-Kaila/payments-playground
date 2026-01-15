from payments.services.base import transition_payment_state
from payments.models import PaymentStatus

def initiate_paystack_payment(transaction, email):
    payload = {
        "email": email,
        "amount": int(transaction.amount * 100),
        "refrence": transaction.reference,
    }

    transaction.raw_request = payload
    transaction.save(update_fields=["raw_request"])
    
    transition_payment_state(
        transaction,
        PaymentStatus.PENDING,
        event_type="PAYSTACK_INITIATED",
        payload=payload,
    )

    return{
        "authorization_url": "https://paystack.test/checkout",
        "refrence": transaction.refrence,
    }