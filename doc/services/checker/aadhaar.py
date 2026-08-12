def verify_aadhaar(extracted_data):

    aadhaar_number = extracted_data.get(
        "aadhaar_number"
    )

    if not aadhaar_number:

        return {
            "status": "VERIFICATION_ERROR",
            "verified": False,
            "reason": "Aadhaar number not found in OCR data.",
        }

    # TODO:
    # Call authorized Aadhaar verification service here.
    #
    # Do NOT store the complete API response.
    #
    # Compare the temporary API response
    # against extracted_data.
    #
    # Then discard the sensitive API response.

    return {
        "status": "VERIFICATION_ERROR",
        "verified": False,
        "reason": "Aadhaar verification API is not configured.",
    }