from payments.models import PaymentStatus, PaymentTransaction, PaymentEvent
from django.utils import timezone

# Define alllowed transitions of states

ALLOWED_TRANSITIONS = {
    PaymentStatus.CREATED: {PaymentStatus.PENDING},
    PaymentStatus.PENDING: {PaymentStatus.SUCCESS, PaymentStatus.FAILED},
    PaymentStatus.SUCCESS:set(), # An empty set, terminal state saying if success done, no double success
    PaymentStatus.FAILED:set(),
}

# Transition function
def transition_payment_state(
    transaction: PaymentTransaction, # the model we are to update
    new_status: str,
    event_type: str,
    payload: dict | None = None,
):

    current_status = transaction.status

    if new_status not in ALLOWED_TRANSITIONS[current_status]:
       raise ValueError(
           f"Invalid transition from {current_status} to {new_status}"
        )

    transaction.status = new_status
    transaction.updated_at = timezone.now()
    transaction.save(update_fields=["status", "updated_at"])
    