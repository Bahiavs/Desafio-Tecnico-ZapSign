from django.test import TestCase
from ..models import Document, Signer, Company
from ..usecases.delete_doc import DeleteDoc


class DeleteDocTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company")
        self.document = Document.objects.create(
            companyID=self.company,
            name="Test Document",
            status="initial"
        )
        self.signer = Signer.objects.create(
            documentID=self.document,
            name="John Doe",
            email="john@example.com",
            status="pending"
        )
        self.delete_doc = DeleteDoc()

    def test_delete_doc(self):
        self.assertTrue(Document.objects.filter(id=self.document.id).exists())
        result = self.delete_doc.execute(doc_id=self.document.id)
        self.assertFalse(Document.objects.filter(id=self.document.id).exists())
        self.assertTrue(result)

    def test_delete_nonexistent_doc(self):
        with self.assertRaises(Document.DoesNotExist):
            self.delete_doc.execute(doc_id=9999)  # Assuming ID 9999 doesn't exist
