from ...models import MockVerificationRecord


def mock_api_lookup(
    document_type,
    extracted_data,
):

    identifier = None

    if document_type == "aadhaar":

        identifier = extracted_data.get(
            "aadhaar_number"
        )

    elif document_type == "pan":

        identifier = extracted_data.get(
            "pan_number"
        )

    elif document_type == "passport":

        identifier = extracted_data.get(
            "passport_number"
        )

    elif document_type == "driving_license":

        identifier = extracted_data.get(
            "license_number"
        )

    if not identifier:

        return {
            "found": False,
            "data": {},
            "reason": (
                "Required document identifier "
                "was not extracted."
            ),
        }

    record = MockVerificationRecord.objects.filter(
        document_type=document_type,
        identifier=identifier,
        enabled=True,
    ).first()

    if not record:

        return {
            "found": False,
            "data": {},
            "reason": (
                "Document was not found in "
                "verification database."
            ),
        }

    return {
        "found": True,
        "data": record.data,
        "reason": "Record found.",
    }