def verify_passport(extracted_data):

    passport_number = extracted_data.get(
        "passport_number"
    )

    if not passport_number:

        return {
            "status": "VERIFICATION_ERROR",
            "verified": False,
            "reason": "Passport number not found in OCR data.",
        }

    # TODO:
    # Authorized passport verification API.

    return {
        "status": "VERIFICATION_ERROR",
        "verified": False,
        "reason": "Passport verification API is not configured.",
    }