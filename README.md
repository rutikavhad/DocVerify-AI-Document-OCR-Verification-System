

<div align="center">
📄 DocVerify — AI Document OCR & Verification System

Secure Document OCR, Information Extraction & Verification Platform

<img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Django-5.2-green?logo=django&logoColor=white" />
<img src="https://img.shields.io/badge/Django%20REST%20Framework-API-red?logo=django" />
<img src="https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql" />
<img src="https://img.shields.io/badge/PaddleOCR-OCR-orange" />
<img src="https://img.shields.io/badge/PyMuPDF-PDF%20Processing-purple" />
<img src="https://img.shields.io/badge/Bootstrap-UI-7952B3?logo=bootstrap&logoColor=white" />

Document processing platform for PDF/image OCR, document-specific information extraction, and secure verification.

</div>

📖 Overview

DocVerify is a Django-based document OCR and verification system for processing PDF and image documents and converting their contents into structured information.

The platform supports:

PDF/image upload

Document-type selection

OCR extraction

Document-specific information extraction

Structured JSON storage

Document verification

Document-specific checker routing

Local mock verification for development

Field comparison and match scoring

Safe VERIFIED / NOT_VERIFIED results

The current verification layer uses a local mock database so the complete workflow can be tested without an external API. It is designed to be replaced later by authorized official organization APIs.

✨ Features

Category

Features

📄 Document Input

PDF, PNG, JPG, JPEG

🔎 OCR

OCR for images and scanned PDFs

🧠 Information Extraction

Document-specific field extraction

🪪 Document Types

Aadhaar, PAN, Passport, Driving Licence, Voter ID, ATM, Invoice, Receipt, Other

🧾 JSON Data

Structured extracted information

🔐 Verification

Document-specific verification pipeline

🧪 Mock API

Local verification database

📊 Comparison

Field matching and verification score

👤 Authentication

Login, registration, logout

👨‍💼 Profile

Profile editing and password management

🗂 History

Search, view, download, verify and delete

✏️ Document Management

Change document type

🖥 Dashboard

Processing and verification statistics

🔌 REST API

Django REST Framework endpoints

🗄 Database

PostgreSQL

🏗️ System Architecture

graph TD

User --> Dashboard
Dashboard --> Upload
Upload --> PDFImage
PDFImage --> OCR
OCR --> RawText
RawText --> InformationExtractor
InformationExtractor --> ExtractedJSON
ExtractedJSON --> DocumentDatabase

User --> Verify
Verify --> Executor
Executor --> DocumentChecker
DocumentChecker --> MockAPI
MockAPI --> APIData
APIData --> Comparator
ExtractedJSON --> Comparator
Comparator --> VerificationResult
VerificationResult --> DocumentDatabase

DocumentDatabase[(PostgreSQL)]

🔄 Document Processing Workflow

PDF / Image
    ↓
File Validation
    ↓
OCR
    ↓
Raw Text
    ↓
Document-Specific Information Extractor
    ↓
Structured JSON
    ↓
PostgreSQL

Example:

{
    "document_type": "pan",
    "pan_number": "QFVPS0764H",
    "name": "SAMAD",
    "dob": "03/02/2004"
}

🔐 Verification Workflow

Stored OCR Text
       ↓
Information Extractor
       ↓
Required Verification Fields
       ↓
Verification Executor
       ↓
Document-Specific Checker
       ↓
Mock Verification API
       ↓
Authoritative Test Data
       ↓
Comparator
       ↓
Match Score
       ↓
VERIFIED / NOT_VERIFIED

The system is designed to return a safe verification result instead of exposing unnecessary sensitive API response data.

Example:

{
    "status": "VERIFIED",
    "score": 100,
    "threshold": 80,
    "matched_fields": 3,
    "compared_fields": 3
}

🧠 Document-Specific Information Extraction

Different documents have different structures and verification fields.

The extractor is therefore document-type aware.

PAN

{
    "document_type": "pan",
    "pan_number": "QFVPS0764H",
    "name": "SAMAD",
    "dob": "03/02/2004"
}

Aadhaar

{
    "document_type": "aadhaar",
    "aadhaar_number": "123456789012",
    "name": "PERSON NAME",
    "dob": "01/01/2000",
    "gender": "MALE"
}

Additional document-specific extraction rules can be added as required.

🧪 Local Mock Verification API

The current project uses a MockVerificationRecord database model to simulate an external verification API.

Example:

Document Type:
PAN

Identifier:
QFVPS0764H

Data:
{
    "pan_number": "QFVPS0764H",
    "name": "SAMAD",
    "dob": "03/02/2004"
}

This allows the entire verification pipeline to be tested without a real external API.

Production transition

The intended architecture is:

Mock Verification
        ↓
Official Organization / Government API

The OCR and information-extraction layers remain independent from the external API.

📊 Verification Statuses

PENDING
PROCESSING
COMPLETED
VERIFYING
VERIFIED
NOT_VERIFIED
VERIFICATION_ERROR
FAILED

Status

Meaning

PENDING

Processing has not started

PROCESSING

OCR/document processing is running

COMPLETED

OCR and extraction completed

VERIFYING

Verification is running

VERIFIED

Verification information matched

NOT_VERIFIED

Verification failed or did not sufficiently match

VERIFICATION_ERROR

Verification service/checker failed

FAILED

Document processing/OCR failed

📁 Project Structure

DocVerify/
│
├── acc/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── doc/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   │
│   ├── services/
│   │   ├── extractor.py
│   │   ├── image.py
│   │   ├── pdf.py
│   │   ├── information_extractor.py
│   │   │
│   │   └── checker/
│   │       ├── executor.py
│   │       ├── mock_api.py
│   │       ├── aadhaar.py
│   │       ├── pan.py
│   │       ├── passport.py
│   │       ├── driving_license.py
│   │       ├── voter_id.py
│   │       └── atm.py
│   │
│   └── migrations/
│
├── Doc_checker/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── base.html
│   ├── dashboard/
│   │   ├── dashboard.html
│   │   ├── document.html
│   │   ├── history.html
│   │   └── change_document_type.html
│   ├── includes/
│   │   ├── navbar.html
│   │   └── sidebar.html
│   └── account/
│       ├── login.html
│       ├── register.html
│       └── profile.html
│
├── static/
│   └── css/
│
├── media/
├── manage.py
├── requirements.txt
└── README.md

🚀 Technologies Used

Backend

Python 3.11+

Django 5.2

Django REST Framework

Database

PostgreSQL

OCR & Document Processing

PaddleOCR

PyMuPDF

PDF rendering

Image processing

Frontend

HTML

CSS

Bootstrap

Django Templates

JavaScript

Authentication

Django Authentication

Session-based authentication

🚀 Installation

Clone Repository

git clone https://github.com/YOUR_USERNAME/DocVerify-AI-Document-OCR-Verification-System.git

cd DocVerify-AI-Document-OCR-Verification-System

Create Virtual Environment

Linux:

python3 -m venv .venv
source .venv/bin/activate

Windows:

python -m venv .venv
.venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

⚙️ PostgreSQL Configuration

Create a PostgreSQL database:

CREATE DATABASE docverify;

Configure the database in:

Doc_checker/settings.py

Example:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "docverify",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

For production, use environment variables or a secure secret-management system.

🗄️ Database Migration

python manage.py makemigrations
python manage.py migrate

Create an admin account:

python manage.py createsuperuser

▶️ Run Application

python manage.py runserver

Open:

http://127.0.0.1:8000/

🧪 Test Verification

Start Django shell:

python manage.py shell

Create a mock PAN verification record:

from doc.models import MockVerificationRecord

MockVerificationRecord.objects.create(
    document_type="pan",
    identifier="QFVPS0764H",
    data={
        "pan_number": "QFVPS0764H",
        "name": "SAMAD",
        "dob": "03/02/2004"
    }
)

Exit:

exit()

Then:

Dashboard
    ↓
Upload PAN
    ↓
OCR
    ↓
Information Extraction
    ↓
Verify
    ↓
Mock Verification Database
    ↓
Comparison
    ↓
VERIFIED / NOT_VERIFIED

🔎 Test OCR and Information Extraction

python manage.py shell

from doc.services.extractor import extract_document
from doc.services.information_extractor import extract_information

text = extract_document("media/test_pan.jpg")

print(text)

data = extract_information(
    document_type="pan",
    raw_text=text,
)

print(data)

Expected structure:

{
    "document_type": "pan",
    "pan_number": "QFVPS0764H",
    "name": "SAMAD",
    "dob": "03/02/2004"
}

🔌 REST API

The project includes Django REST Framework endpoints for:

Document upload

Document listing

Document details

Document deletion

Document search

Dashboard statistics

Protected endpoints require authentication.

🗂️ Document History

The History section provides:

Uploaded document list

Search

Document type

Processing status

View document

Download document

Delete document

Change document type

Verify document

👤 User Account

The account system provides:

Registration

Login

Logout

Profile view/edit

Password management

🔐 Security

Document verification can involve sensitive identity information.

The intended production architecture is:

Authenticated User
        ↓
Dashboard
        ↓
Document
        ↓
OCR
        ↓
Required Verification Fields
        ↓
Secure Verification API
        ↓
Comparison
        ↓
Safe Verification Result

API credentials must never be committed to GitHub.

Use environment variables or secure application settings for:

API_KEY
API_SECRET
CLIENT_ID
CLIENT_SECRET

The planned settings section can also protect sensitive API configuration with additional authentication such as 2FA.

⚠️ Current Development Limitation

The current verification system uses a local mock verification database.

It does not represent a real government or organization verification service.

Real verification APIs should only be integrated after obtaining the required authorization, documentation, credentials, and permitted use.

When an official API becomes available, the intended change is primarily inside the document-specific checker layer:

checker/
├── aadhaar.py
├── pan.py
├── passport.py
├── driving_license.py
└── ...

The OCR and information-extraction architecture can remain independent from the external API.

🔮 Future Enhancements

Official document verification API integration

Secure API credential management

Two-factor authentication for API settings

Document-specific API request builders

Strong primary-identifier verification

Improved field normalization

OCR error correction

QR-code/document metadata verification

Verification audit logs

API rate limiting

Background processing with Celery/Redis

Encryption for sensitive stored data

Role-based organization access

Multi-organization verification

Docker deployment

Cloud deployment

🤝 Contributing

Contributions are welcome.

git checkout -b feature/your-feature

git add .
git commit -m "Add your feature"
git push origin feature/your-feature

Then open a Pull Request.

📜 License

Distributed under the MIT License.

👨‍💻 Author

Rutik Avhad

Python Developer | Cybersecurity Enthusiast | AI Application Developer

<div align="center">

⭐ Star the Project

If you find DocVerify useful, consider giving the repository a ⭐.

Built with ❤️ using

Python • Django • PostgreSQL • PaddleOCR • PyMuPDF • Bootstrap

</div>
