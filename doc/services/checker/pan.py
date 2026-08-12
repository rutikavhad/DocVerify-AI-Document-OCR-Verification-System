def verify_pan(extracted_data):

    pan_number = extracted_data.get(
        "pan_number"
    )

    if not pan_number:

        return {
            "status": "VERIFICATION_ERROR",
            "verified": False,
            "reason": "PAN number not found in OCR data.",
        }

    # TODO:
    # Call authorized PAN verification service.
    # Compare response with extracted_data.
    # Do not persist sensitive response.

    return {
        "status": "VERIFICATION_ERROR",
        "verified": False,
        "reason": "PAN verification API is not configured.",
    }