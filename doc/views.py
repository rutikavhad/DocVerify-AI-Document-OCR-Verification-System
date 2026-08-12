from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Document
from .serializers import DocumentSerializer
from .services.extractor import extract_document
from .services.checker.executor import execute_verification
from django.contrib import messages

from .services.information_extractor import (
    extract_information,
)
from .services.checker.executor import execute_verification


# ============================================================
# API - UPLOAD DOCUMENT
# ============================================================

class UploadDocumentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        document_type = request.data.get(
            "document_type",
            "other",
        )

        document = Document.objects.create(
            owner=request.user,
            file=uploaded_file,
            original_filename=uploaded_file.name,
            file_type=Path(
                uploaded_file.name
            ).suffix.lower(),
            document_type=document_type,
            status=Document.Status.PROCESSING,
        )

        try:

            # -----------------------------
            # OCR
            # -----------------------------

            text = extract_document(
                document.file.path
            )

            document.raw_text = text

            document.ocr_result = {
                "document_type": document_type,
                "text": text,
            }

            document.status = Document.Status.COMPLETED

            document.save()

            serializer = DocumentSerializer(
                document
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            document.status = Document.Status.FAILED

            document.save()

            return Response(
                {
                    "status": "FAILED",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ============================================================
# API - DOCUMENT LIST
# ============================================================

class DocumentListAPIView(generics.ListAPIView):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Document.objects.filter(
            owner=self.request.user
        ).order_by("-created_at")


# ============================================================
# API - DOCUMENT DETAIL
# ============================================================

class DocumentDetailAPIView(
    generics.RetrieveAPIView
):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Document.objects.filter(
            owner=self.request.user
        )


# ============================================================
# API - DOCUMENT DELETE
# ============================================================

class DocumentDeleteAPIView(
    generics.DestroyAPIView
):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Document.objects.filter(
            owner=self.request.user
        )


# ============================================================
# API - SEARCH DOCUMENT
# ============================================================

class SearchDocumentAPIView(
    generics.ListAPIView
):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        query = self.request.GET.get(
            "q",
            "",
        ).strip()

        queryset = Document.objects.filter(
            owner=self.request.user
        )

        if query:

            queryset = queryset.filter(
                raw_text__icontains=query
            )

        return queryset.order_by(
            "-created_at"
        )


# ============================================================
# API - DASHBOARD STATISTICS
# ============================================================

class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        qs = Document.objects.filter(
            owner=request.user
        )

        return Response({

            "total_documents": qs.count(),

            "verified": qs.filter(
                status=Document.Status.VERIFIED
            ).count(),

            "not_verified": qs.filter(
                status__in=[
                    Document.Status.COMPLETED,
                    Document.Status.NOT_VERIFIED,
                ]
            ).count(),

            "verifying": qs.filter(
                status=Document.Status.VERIFYING
            ).count(),

            "verification_errors": qs.filter(
                status__in=[
                    Document.Status.FAILED,
                    Document.Status.VERIFICATION_ERROR,
                ]
            ).count(),

        })


# ============================================================
# WEB - DASHBOARD
# ============================================================

@login_required(login_url="login")
def dashboard(request):

    result = None

    if request.method == "POST":

        uploaded_file = request.FILES.get(
            "file"
        )

        document_type = request.POST.get(
            "document_type",
            "other",
        )

        action = request.POST.get(
            "action",
            "extract",
        )

        # ----------------------------------------
        # Check file
        # ----------------------------------------

        if not uploaded_file:

            result = {
                "status": "FAILED",
                "error": "No file uploaded.",
            }

        else:

            file_extension = Path(
                uploaded_file.name
            ).suffix.lower()

            # ----------------------------------------
            # Allow only PDF/images
            # ----------------------------------------

            allowed_extensions = [
                ".pdf",
                ".png",
                ".jpg",
                ".jpeg",
            ]

            if file_extension not in allowed_extensions:

                result = {
                    "status": "FAILED",
                    "error": (
                        "Unsupported file type. "
                        "Only PDF, PNG, JPG and JPEG "
                        "are allowed."
                    ),
                }

            else:

                # ----------------------------------------
                # Create document
                # ----------------------------------------

                document = Document.objects.create(

                    owner=request.user,

                    file=uploaded_file,

                    original_filename=(
                        uploaded_file.name
                    ),

                    file_type=file_extension,

                    document_type=document_type,

                    status=Document.Status.PROCESSING,
                )

                try:

                    # ====================================
                    # STEP 1 - OCR
                    # ====================================

                    text = extract_document(
                        document.file.path
                    )

                    document.raw_text = text

                    document.ocr_result = {

                        "document_type":
                            document_type,

                        "action":
                            action,

                        "text":
                            text,
                    }

                    # ====================================
                    # EXTRACT ONLY
                    # ====================================

                    if action == "extract":

                        document.status = (
                            Document.Status.COMPLETED
                        )

                        document.save()

                        result = {

                            "status": "COMPLETED",

                            "document_type":
                                document_type,

                            "text":
                                text,
                        }

                    # ====================================
                    # VERIFY DOCUMENT
                    # ====================================

                    elif action == "verify":

                        # --------------------------------
                        # OCR completed
                        # --------------------------------

                        document.status = (
                            Document.Status.VERIFYING
                        )

                        document.save()

                        # --------------------------------
                        # Get extracted data
                        # --------------------------------
                        #
                        # For now we use ocr_result.
                        #
                        # Later your document-specific
                        # extractor can produce:
                        #
                        # {
                        #     "aadhaar_number": "...",
                        #     "name": "...",
                        #     "dob": "..."
                        # }
                        #

                        extracted_data = extract_information(
                            document_type=document_type,
                            raw_text=text,
                        )

                        document.extracted_data = extracted_data
                        # --------------------------------
                        # Execute verifier
                        # --------------------------------

                        verification = execute_verification(
                            document_type=document_type,
                            extracted_data=extracted_data,
                        )

                        # --------------------------------
                        # Save ONLY verification result
                        # --------------------------------

                        document.verification_result = (
                            verification
                        )

                        verification_status = (
                            verification.get(
                                "status",
                                "VERIFICATION_ERROR",
                            )
                        )

                        # --------------------------------
                        # Make sure status is valid
                        # --------------------------------

                        valid_statuses = [

                            Document.Status.VERIFIED,

                            Document.Status.NOT_VERIFIED,

                            Document.Status.VERIFICATION_ERROR,

                        ]

                        if (
                            verification_status
                            not in valid_statuses
                        ):

                            verification_status = (
                                Document.Status.VERIFICATION_ERROR
                            )

                        document.status = (
                            verification_status
                        )

                        document.save()

                        # --------------------------------
                        # Result for webpage
                        # --------------------------------

                        result = {

                            "status": (
                                verification_status
                            ),

                            "document_type": (
                                document_type
                            ),

                            "verification": (
                                verification
                            ),
                        }

                    # ====================================
                    # UNKNOWN ACTION
                    # ====================================

                    else:

                        document.status = (
                            Document.Status.FAILED
                        )

                        document.save()

                        result = {

                            "status": "FAILED",

                            "error": (
                                "Invalid action."
                            ),
                        }

                except Exception as e:

                    # ------------------------------------
                    # Processing failed
                    # ------------------------------------

                    document.status = (
                        Document.Status.FAILED
                    )

                    document.save()

                    result = {

                        "status": "FAILED",

                        "error": str(e),
                    }

    # ========================================================
    # DASHBOARD STATISTICS
    # ========================================================

    documents_queryset = Document.objects.filter(
        owner=request.user
    )

    stats = {

        "total": documents_queryset.count(),

        "verified": documents_queryset.filter(
            status=Document.Status.VERIFIED,
        ).count(),

        "not_verified": documents_queryset.filter(
            status__in=[
                Document.Status.COMPLETED,
                Document.Status.NOT_VERIFIED,
            ],
        ).count(),

        "errors": documents_queryset.filter(
            status__in=[
                Document.Status.FAILED,
                Document.Status.VERIFICATION_ERROR,
            ],
        ).count(),

    }

    # ========================================================
    # RECENT DOCUMENTS
    # ========================================================

    recent_documents = (
        documents_queryset
        .order_by("-created_at")[:10]
    )

    # ========================================================
    # RENDER
    # ========================================================

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "stats": stats,
            "result": result,
            "documents": recent_documents,
        },
    )


# ============================================================
# WEB - DOCUMENT DETAIL
# ============================================================

@login_required(login_url="login")
def document_detail(request, pk):

    document = get_object_or_404(
        Document,
        pk=pk,
        owner=request.user,
    )

    return render(
        request,
        "dashboard/document.html",
        {
            "document": document,
        },
    )


# ============================================================
# WEB - DOCUMENT DELETE
# ============================================================

@login_required(login_url="login")
def document_delete(request, pk):

    document = get_object_or_404(
        Document,
        pk=pk,
        owner=request.user,
    )

    if request.method != "POST":

        return redirect(
            "history"
        )

    # Delete physical file
    if document.file:

        document.file.delete(
            save=False
        )

    # Delete database record
    document.delete()

    messages.success(
        request,
        "Document deleted successfully.",
    )

    return redirect(
        "history"
    )

# ============================================================
# WEB - HISTORY
# ============================================================

@login_required(login_url="login")
def history(request):

    query = request.GET.get("q", "").strip()

    documents = Document.objects.filter(
        owner=request.user
    )

    if query:

        documents = documents.filter(
            original_filename__icontains=query
        )

    documents = documents.order_by(
        "-created_at"
    )

    return render(
        request,
        "dashboard/history.html",
        {
            "documents": documents,
            "query": query,
        },
    )


@login_required(login_url="login")
def change_document_type(request, pk):

    document = get_object_or_404(
        Document,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":

        document_type = request.POST.get(
            "document_type"
        )

        valid_types = [
            choice[0]
            for choice in Document.DocumentType.choices
        ]

        if document_type not in valid_types:

            messages.error(
                request,
                "Invalid document type.",
            )

            return redirect(
                "change_document_type",
                pk=pk,
            )

        # ---------------------------------------
        # Change document type
        # ---------------------------------------

        document.document_type = document_type

        # Previous verification is no longer valid
        document.verification_result = {}

        # OCR still exists, but verification needs
        # to be performed again using the new type.

        if document.raw_text:

            document.status = (
                Document.Status.COMPLETED
            )

        else:

            document.status = (
                Document.Status.PENDING
            )

        document.save()

        messages.success(
            request,
            "Document type updated successfully.",
        )

        return redirect(
            "history"
        )

    return render(
        request,
        "dashboard/change_document_type.html",
        {
            "document": document,
            "document_types": (
                Document.DocumentType.choices
            ),
        },
    )


#varify doc main part

@login_required(login_url="login")
def verify_document(request, pk):

    document = get_object_or_404(
        Document,
        pk=pk,
        owner=request.user,
    )

    if request.method != "POST":

        return redirect("history")

    # =====================================================
    # CHECK OCR
    # =====================================================

    if not document.raw_text:

        messages.error(
            request,
            "OCR data is not available for this document.",
        )

        return redirect("history")

    # =====================================================
    # EXTRACT REQUIRED INFORMATION
    # =====================================================

    try:

        extracted_data = extract_information(
            document_type=document.document_type,
            raw_text=document.raw_text,
        )

    except Exception:

        document.status = (
            Document.Status.VERIFICATION_ERROR
        )

        document.save()

        messages.error(
            request,
            "Information extraction failed.",
        )

        return redirect("history")

    # =====================================================
    # CHECK REQUIRED INFORMATION
    # =====================================================

    if not extracted_data:

        document.status = (
            Document.Status.NOT_VERIFIED
        )

        document.extracted_data = {}

        document.save()

        messages.warning(
            request,
            "No verification information could be extracted.",
        )

        return redirect("history")

    # =====================================================
    # SAVE EXTRACTED INFORMATION
    # =====================================================

    document.extracted_data = extracted_data

    document.status = (
        Document.Status.VERIFYING
    )

    document.save()

    # =====================================================
    # CALL CHECKER
    # =====================================================

    try:

        verification = execute_verification(

            document_type=(
                document.document_type
            ),

            extracted_data=(
                extracted_data
            ),
        )

    except Exception:

        document.status = (
            Document.Status.VERIFICATION_ERROR
        )

        document.verification_result = {
            "status": "VERIFICATION_ERROR",
            "reason": "Verification service failed.",
        }

        document.save()

        messages.error(
            request,
            "Verification service failed.",
        )

        return redirect("history")

    # =====================================================
    # SAVE SAFE RESULT ONLY
    # =====================================================

    verification_status = verification.get(
        "status",
        Document.Status.VERIFICATION_ERROR,
    )

    if verification_status not in [
        Document.Status.VERIFIED,
        Document.Status.NOT_VERIFIED,
        Document.Status.VERIFICATION_ERROR,
    ]:

        verification_status = (
            Document.Status.VERIFICATION_ERROR
        )

    document.status = verification_status

    document.verification_result = verification

    document.save()

    # =====================================================
    # USER MESSAGE
    # =====================================================

    if verification_status == Document.Status.VERIFIED:

        messages.success(
            request,
            (
                "Document verified successfully. "
                f"Match score: "
                f"{verification.get('score', 0)}%"
            ),
        )

    elif verification_status == Document.Status.NOT_VERIFIED:

        messages.warning(
            request,
            (
                "Document could not be verified. "
                f"Match score: "
                f"{verification.get('score', 0)}%"
            ),
        )

    else:

        messages.error(
            request,
            "Verification could not be completed.",
        )

    return redirect(
        "document_detail",
        pk=document.pk,
    )

# ============================================================
# LOGOUT
# ============================================================

def logout_view(request):

    logout(request)

    return redirect("login")