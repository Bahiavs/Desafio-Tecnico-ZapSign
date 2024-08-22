from django.test import TestCase
from django.utils import timezone

from documentapp.models import Company, Document, Signer
from documentapp.usecases.get_docs import GetDocs


class GetDocsTestCase(TestCase):
    def setUp(self):
        self.get_docs = GetDocs()
        self.company = Company.objects.create(name="Test Company")
        self.document1 = Document.objects.create(
            companyID=self.company,
            name="Document 1",
            status="initial",
            created_at=timezone.now(),
            created_by="creator@example.com"
        )
        self.document2 = Document.objects.create(
            companyID=self.company,
            name="Document 2",
            status="completed",
            created_at=timezone.now(),
            created_by="creator@example.com"
        )
        Signer.objects.create(documentID=self.document1, name="Signer 1", email="signer1@example.com", status="pending")
        Signer.objects.create(documentID=self.document1, name="Signer 2", email="signer2@example.com", status="signed")
        Signer.objects.create(documentID=self.document2, name="Signer 3", email="signer3@example.com", status="pending")

    def test_get_docs(self):
        documents_list = self.get_docs.execute()
        expected = [
            {
                'documentID': self.document1.id,
                'name': self.document1.name,
                'status': self.document1.status,
                'createdAt': self.document1.created_at,
                'createdBy': self.document1.created_by,
                'signers': [
                    {'name': 'Signer 1', 'email': 'signer1@example.com', 'status': 'pending',
                     'id': Signer.objects.get(name="Signer 1").id},
                    {'name': 'Signer 2', 'email': 'signer2@example.com', 'status': 'signed',
                     'id': Signer.objects.get(name="Signer 2").id},
                ]
            },
            {
                'documentID': self.document2.id,
                'name': self.document2.name,
                'status': self.document2.status,
                'createdAt': self.document2.created_at,
                'createdBy': self.document2.created_by,
                'signers': [
                    {'name': 'Signer 3', 'email': 'signer3@example.com', 'status': 'pending',
                     'id': Signer.objects.get(name="Signer 3").id},
                ]
            }
        ]
        self.assertEqual(documents_list, expected)
