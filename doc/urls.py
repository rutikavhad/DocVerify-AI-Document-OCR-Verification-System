from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import UploadDocumentAPIView

from .views import (
    UploadDocumentAPIView,
    DocumentListAPIView,
    DocumentDetailAPIView,
    DocumentDeleteAPIView,
    SearchDocumentAPIView,
)
from django.urls import path
from . import views


urlpatterns = [
    #api
    path("upload/", UploadDocumentAPIView.as_view()),
    path("", DocumentListAPIView.as_view()),
    path("<int:pk>/", DocumentDetailAPIView.as_view()),
    path("<int:pk>/delete/", DocumentDeleteAPIView.as_view()),
    path("search/", SearchDocumentAPIView.as_view()),

    #normal
    path("dashboard/",views.dashboard,name="dashboard",),
    path("history/",views.history,name="history",),
    path("document/<int:pk>/",views.document_detail,name="document_detail",),
    path("document/<int:pk>/verify/",views.verify_document,name="verify_document",),
    path("document/<int:pk>/change-type/",views.change_document_type,name="change_document_type",),
    path("document/<int:pk>/delete/",views.document_delete,name="document_delete",),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )