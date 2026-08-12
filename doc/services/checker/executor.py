from .mock_api import mock_api_lookup

from ..comparator import compare_information


def execute_verification(
    document_type,
    extracted_data,
):


    api_response = mock_api_lookup(
        document_type=document_type,
        extracted_data=extracted_data,
    )


    # ==========================================
    # 2. Record not found
    # ==========================================

    if not api_response["found"]:

        return {
            "status": "NOT_VERIFIED",
            "score": 0,
            "threshold": 80,
            "matched_fields": 0,
            "compared_fields": 0,
            "reason": api_response["reason"],
        }


    # ==========================================
    # 3. Get API data
    # ==========================================

    api_data = api_response["data"]


    # ==========================================
    # 4. Compare OCR information with API
    # ==========================================

    comparison = compare_information(
        extracted_data=extracted_data,
        api_data=api_data,
    )


    # ==========================================
    # 5. Final result
    # ==========================================

    if comparison["valid"]:

        final_status = "VERIFIED"

    else:

        final_status = "NOT_VERIFIED"


    # ==========================================
    # 6. Return SAFE result
    # ==========================================

    return {

        "status": final_status,

        "score": comparison["score"],

        "threshold": comparison["threshold"],

        "matched_fields":
            comparison["matched_fields"],

        "compared_fields":
            comparison["compared_fields"],

        "fields":
            comparison["fields"],

        "reason": (
            "Information matched."
            if comparison["valid"]
            else
            "Information did not match."
        ),
    }