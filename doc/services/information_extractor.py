import re


# ============================================================
# COMMON HELPERS
# ============================================================

def clean_text(text):
    """
    Normalize OCR text so regex matching becomes easier.
    """

    if not text:
        return ""

    text = text.replace("\n", " ")

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def normalize_name(value):
    """
    Normalize a person's name for comparison.
    """

    if not value:
        return ""

    value = value.upper()

    value = re.sub(
        r"[^A-Z ]",
        "",
        value,
    )

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    return value.strip()


def normalize_number(value):
    """
    Remove spaces and non-alphanumeric characters.
    """

    if not value:
        return ""

    return re.sub(
        r"[^A-Z0-9]",
        "",
        value.upper(),
    )


def normalize_date(value):
    """
    Normalize common date formats.
    """

    if not value:
        return ""

    value = value.strip()

    value = value.replace(
        ".",
        "/",
    )

    value = value.replace(
        "-",
        "/",
    )

    return value


# ============================================================
# NAME
# ============================================================

def extract_name(text):

    patterns = [

        r"(?:NAME|नाम)\s*[:\-]?\s*([A-Z][A-Z .]{2,})",

        r"(?:NAME OF HOLDER)\s*[:\-]?\s*([A-Z][A-Z .]{2,})",

        r"(?:CARD HOLDER)\s*[:\-]?\s*([A-Z][A-Z .]{2,})",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            name = match.group(1).strip()

            # Stop common fields accidentally captured
            stop_words = [
                "DOB",
                "DATE",
                "GENDER",
                "ADDRESS",
                "FATHER",
                "MOTHER",
                "S/O",
                "D/O",
            ]

            for word in stop_words:

                name = re.split(
                    rf"\b{word}\b",
                    name,
                    flags=re.IGNORECASE,
                )[0]

            name = normalize_name(name)

            if len(name) >= 3:

                return name

    return None


# ============================================================
# DATE OF BIRTH
# ============================================================

def extract_dob(text):

    patterns = [

        r"(?:DOB|D\.O\.B|DATE OF BIRTH|BIRTH DATE)"
        r"\s*[:\-]?\s*"
        r"(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{4})",

        r"\b(\d{2}[\/\-]\d{2}[\/\-]\d{4})\b",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            return normalize_date(
                match.group(1)
            )

    return None


# ============================================================
# GENDER
# ============================================================

def extract_gender(text):

    patterns = [

        r"(?:GENDER|SEX)\s*[:\-]?\s*"
        r"(MALE|FEMALE|M|F|OTHER)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            value = match.group(1).upper()

            if value == "M":
                return "MALE"

            if value == "F":
                return "FEMALE"

            return value

    return None


# ============================================================
# AADHAAR NUMBER
# ============================================================

def extract_aadhaar_number(text):

    # 1234 5678 9012
    match = re.search(
        r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        text,
    )

    if match:

        return normalize_number(
            match.group()
        )

    return None


# ============================================================
# PAN NUMBER
# ============================================================

def extract_pan_number(text):

    match = re.search(
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        text.upper(),
    )

    if match:

        return match.group()

    return None


# ============================================================
# PASSPORT NUMBER
# ============================================================

def extract_passport_number(text):

    match = re.search(
        r"\b[A-Z][0-9]{7}\b",
        text.upper(),
    )

    if match:

        return match.group()

    return None


# ============================================================
# DRIVING LICENCE NUMBER
# ============================================================

def extract_driving_license_number(text):

    patterns = [

        r"\b[A-Z]{2}[0-9]{2}"
        r"[A-Z0-9]{4,15}\b",

        r"\b[A-Z]{2}[- ]?[0-9]{2}"
        r"[- ]?[0-9]{4,15}\b",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text.upper(),
        )

        if match:

            return normalize_number(
                match.group()
            )

    return None


# ============================================================
# ADDRESS
# ============================================================

def extract_address(text):

    patterns = [

        r"(?:ADDRESS)\s*[:\-]?\s*(.+?)(?:\bDOB\b|\bDATE\b|\bGENDER\b|$)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            address = match.group(1).strip()

            if len(address) > 5:

                return address

    return None


# ============================================================
# AADHAAR
# ============================================================

def extract_aadhaar(text):

    return {

        "document_type": "aadhaar",

        "aadhaar_number":
            extract_aadhaar_number(text),

        "name":
            extract_name(text),

        "dob":
            extract_dob(text),

        "gender":
            extract_gender(text),

        "address":
            extract_address(text),

    }


# ============================================================
# PAN
# ============================================================

def extract_pan(text):

    return {

        "document_type": "pan",

        "pan_number":
            extract_pan_number(text),

        "name":
            extract_name(text),

        "dob":
            extract_dob(text),

    }


# ============================================================
# PASSPORT
# ============================================================

def extract_passport(text):

    return {

        "document_type": "passport",

        "passport_number":
            extract_passport_number(text),

        "name":
            extract_name(text),

        "dob":
            extract_dob(text),

        "gender":
            extract_gender(text),

    }


# ============================================================
# DRIVING LICENCE
# ============================================================

def extract_driving_license(text):

    return {

        "document_type":
            "driving_license",

        "license_number":
            extract_driving_license_number(text),

        "name":
            extract_name(text),

        "dob":
            extract_dob(text),

    }


# ============================================================
# GENERIC
# ============================================================

def extract_generic(text):

    return {

        "document_type": "other",

        "name":
            extract_name(text),

        "dob":
            extract_dob(text),

        "gender":
            extract_gender(text),

    }


# ============================================================
# MAIN EXECUTOR
# ============================================================

def extract_information(
    document_type,
    raw_text,
):

    text = clean_text(
        raw_text
    )

    extractors = {

        "aadhaar":
            extract_aadhaar,

        "pan":
            extract_pan,

        "passport":
            extract_passport,

        "driving_license":
            extract_driving_license,

    }

    extractor = extractors.get(
        document_type,
        extract_generic,
    )

    data = extractor(
        text
    )

    # Remove fields where extraction failed.
    data = {
        key: value
        for key, value in data.items()
        if value not in [
            None,
            "",
        ]
    }

    return data