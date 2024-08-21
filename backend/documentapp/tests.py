import json
from django.test import TestCase

from .interface_adapters.doc_api.doc_api_fake import DocAPIFake
from .models import Company, Document, Signer
from .usecases.create_document import CreateDocument


class CreateDocumentTestCase(TestCase):

    def setUp(self):
        Company.objects.create(name='Company Name', api_token='')
        doc_api = DocAPIFake()
        self.create_document = CreateDocument(doc_api)

    def test_create_doc(self):
        input_data = json.dumps({
            "name": "Documento A",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [
                {"name": "Signatario A", "email": "signatarioA@email.com"},
                {"name": "Signatario B", "email": "signatarioB@email.com"}
            ]
        })
        response = self.create_document.execute(input_data)
        doc = Document.objects.first()
        signer_a = Signer.objects.get(email='signatarioA@email.com')
        signer_b = Signer.objects.get(email='signatarioB@email.com')
        self.assertEqual(doc.name, "Documento A")
        self.assertEqual(signer_a.email, 'signatarioA@email.com')
        self.assertEqual(signer_b.email, 'signatarioB@email.com')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Document created successfully', response.content.decode())

    def test_doc_missing_field_name(self):
        input_data = json.dumps({
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"name": "Signer Name", "email": "signer@email.com"}]
        })
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required field: name', response.content.decode())

    def test_doc_missing_field_url(self):
        input_data = json.dumps({
            "name": "Doc Name",
            "signers": [{"name": "Signer Name", "email": "signer@email.com"}]
        })
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required field: url', response.content.decode())

    def test_doc_missing_field_signer(self):
        input_data = json.dumps({
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
        })
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required field: signer', response.content.decode())

    def test_doc_invalid_name_type(self):
        input_data = json.dumps({
            "name": 123,
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"name": "Signer Name", "email": "signer@email.com"}]
        })
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('name must be a string', response.content.decode())

    def test_doc_invalid_url_type(self):
        input_data = json.dumps(
            {"name": 'Doc Name', "url": 123, "signers": [{"name": "Signer Name", "email": "signer@email.com"}]}
        )
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('url must be a string', response.content.decode())

    def test_doc_invalid_signer_type(self):
        input_data = json.dumps({
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": 123
        })
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('signers must be a list', response.content.decode())

    def test_doc_empty_signer(self):
        input_data = json.dumps({
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": []
        })
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('signers must have at least 1 item', response.content.decode())

    def test_doc_missing_signer_field_name(self):
        input_data = json.dumps({
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"email": "signer@email.com"}]
        })
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required field in a signer: name', response.content.decode())

    def test_doc_missing_signer_field_email(self):
        input_data = json.dumps({
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"name": "Signer Name"}]
        })
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required field in a signer: email', response.content.decode())

    def test_doc_invalid_signer_name_type(self):
        input_data = json.dumps({
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"name": 123, "email": "signer@email.com"}]
        })
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Signer name must be a string', response.content.decode())

    def test_doc_invalid_signer_email_type(self):
        input_data = json.dumps({
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"name": "Signer Name", "email": 123}]
        })
        response = self.create_document.execute(input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Signer email must be a string', response.content.decode())
