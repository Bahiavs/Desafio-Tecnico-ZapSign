from django.test import TestCase
from ..models import Document
from ..usecases.update_doc import UpdateDoc


class UpdateDocTestCase(TestCase):
    def setUp(self):
        self.document = Document.objects.create(
            name="Old Document",
            status="initial",
            created_by="creator@example.com"
        )
        self.update_doc_service = UpdateDoc()

    def test_update_document_valid(self):
        result = self.update_doc_service.execute(self.document.id, {'name': 'New Document'})
        self.assertTrue(result)
        self.document.refresh_from_db()
        self.assertEqual(self.document.name, 'New Document')

    def test_update_document_invalid_name(self):
        with self.assertRaises(TypeError):
            self.update_doc_service.execute(self.document.id, {'name': 123})

    def test_update_non_existent_document(self):
        with self.assertRaises(Document.DoesNotExist):
            self.update_doc_service.execute(9999, {'name': 'Name'})
