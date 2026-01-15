from payments.services.base import transition_payment_state
from payments.models import PaymentStatus

def initiate_mpesa_payment(transaction, phone_number):
    """
    Initiates an STK push request

    """
    payload = {
        "phone_number": phone_number,
        "amount": str(transaction.amount),
        "refrence": transaction.refrence,
    }

    # store raw request
    transaction.raw_request = payload
    transaction.save(update_fields=[raw_request])

    # Move CREATED -> PENDING
    transaction_payment_state(
        transaction,
        PaymentStatus.PENDING,
        event_type="STK_PUSH_SENT",
        payload=payload,

    )

    return{
        "message": "STK PUSH initiated",
        "refrence": transaction.reference,
    }