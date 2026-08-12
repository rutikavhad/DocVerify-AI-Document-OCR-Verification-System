from django.conf import settings
from django.db import models


class Document(models.Model):

    class Status(models.TextChoices):

        PENDING = "PENDING", "Pending"

        PROCESSING = "PROCESSING", "Processing"

        COMPLETED = "COMPLETED", "Completed"

        VERIFYING = "VERIFYING", "Verifying"

        VERIFIED = "VERIFIED", "Verified"

        NOT_VERIFIED = "NOT_VERIFIED", "Not Verified"

        VERIFICATION_ERROR = (
            "VERIFICATION_ERROR",
            "Verification Error",
        )

        FAILED = "FAILED", "Failed"

    class DocumentType(models.TextChoices):

        AADHAAR = "aadhaar", "Aadhaar"

        PAN = "pan", "PAN"

        PASSPORT = "passport", "Passport"

        DRIVING_LICENSE = (
            "driving_license",
            "Driving Licence",
        )

        VOTER_ID = "voter_id", "Voter ID"

        ATM = "atm", "ATM Card"

        INVOICE = "invoice", "Invoice"

        RECEIPT = "receipt", "Receipt"

        OTHER = "other", "Other"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    file = models.FileField(
        upload_to="documents/%Y/%m/%d/"
    )

    original_filename = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    file_type = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )

    raw_text = models.TextField(
        blank=True
    )

    ocr_result = models.JSONField(
        default=dict
    )

    extracted_data = models.JSONField(
        default=dict
    )

    verification_result = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.original_filename or f"Document {self.pk}"



#test data

from django.conf import settings
from django.db import models


class MockVerificationRecord(models.Model):

    document_type = models.CharField(
        max_length=50
    )

    identifier = models.CharField(
        max_length=100
    )

    data = models.JSONField(
        default=dict
    )

    enabled = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "document_type",
                    "identifier",
                ],
                name="unique_mock_document_identifier",
            )
        ]

    def __str__(self):

        return (
            f"{self.document_type} - "
            f"{self.identifier}"
        )