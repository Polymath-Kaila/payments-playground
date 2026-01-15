from django.db import models
from django.utils import timezone
import uuid

class PaymentProvider(models.TextChoices):
    """
    prevents string typos
    enforces allowed providers
    """
    MPESA = "mpesa", "M-Pesa"
    PAYSTACK = "paystack","Paystack"

class PaymentStatus(models.TextChoices):
    """
    this are the payment states
    """
    CREATED = "created","Created"
    PENDING = "pending","Pending"
    SUCCESS = "success","Success"
    FAILED = "failed","Failed"

class PaymentTransaction(models.Model):
    """
    this is the idempotency key
    used by webhooks
    prevents double processing
    """
    reference = models.CharField(
        max_lenth=100,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique reference used across the system provider"
    )

    provider = models.CharField(
        max_length=20,
        choices=PaymentProvider.choices
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=20,
        default="KES" # Never hardcode currency in logic
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.CREATED # Status only change via backend logic
    )

    raw_request = models.JSONField(
        null=True,
        blandk=True,
        help_text = "Initial request payload sent to provider"
    )

    raw_webhook = models.JSONField(
        null=True,
        blank=True,
        help_text="Last webhook payload received from provider"

    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.reference} ({self.status})"