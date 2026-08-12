from difflib import SequenceMatcher


DEFAULT_THRESHOLD = 80


def normalize_value(value):

    if value is None:
        return ""

    value = str(value).upper().strip()

    # Remove spaces and common punctuation
    value = (
        value
        .replace(" ", "")
        .replace("-", "")
        .replace("/", "")
        .replace(".", "")
    )

    return value


def similarity(value1, value2):

    value1 = normalize_value(
        value1
    )

    value2 = normalize_value(
        value2
    )

    if not value1 or not value2:

        return 0

    if value1 == value2:

        return 100

    return round(
        SequenceMatcher(
            None,
            value1,
            value2,
        ).ratio() * 100,
        2,
    )


def compare_information(
    extracted_data,
    api_data,
    threshold=DEFAULT_THRESHOLD,
):

    results = {}

    total_score = 0
    matched_fields = 0
    compared_fields = 0

    for field, extracted_value in extracted_data.items():

        # document_type isn't a person field
        if field == "document_type":
            continue

        api_value = api_data.get(
            field
        )

        if api_value is None:

            results[field] = {
                "matched": False,
                "score": 0,
            }

            compared_fields += 1

            continue

        score = similarity(
            extracted_value,
            api_value,
        )

        matched = (
            score >= threshold
        )

        results[field] = {

            "matched": matched,

            "score": score,

        }

        total_score += score

        compared_fields += 1

        if matched:

            matched_fields += 1

    if compared_fields:

        overall_score = round(
            total_score / compared_fields,
            2,
        )

    else:

        overall_score = 0

    valid = (
        compared_fields > 0
        and overall_score >= threshold
    )

    return {

        "valid": valid,

        "score": overall_score,

        "threshold": threshold,

        "matched_fields":
            matched_fields,

        "compared_fields":
            compared_fields,

        "fields":
            results,
    }