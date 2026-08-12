def verify_driving_license(extracted_data):

    license_number = extracted_data.get(
        "license_number"
    )

    if not license_number:

        return {
            "status": "VERIFICATION_ERROR",
            "verified": False,
            "reason": (
                "Driving licence number "
                "not found in OCR data."
            ),
        }

    # TODO:
    # Authorized driving licence verification API.

    return {
        "status": "VERIFICATION_ERROR",
        "verified": False,
        "reason": (
            "Driving licence verification "
            "API is not configured."
        ),
    }