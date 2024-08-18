from django.urls import path
from . import views

urlpatterns = [
    path("create", views.create_document, name="create_document"),
    path("read", views.get_documents, name="get_documents"),
    path('delete/<int:document_id>', views.delete_document, name='delete_document'),
    path('update-signer/<int:signer_id>', views.update_signer, name='update_signer'),
]
