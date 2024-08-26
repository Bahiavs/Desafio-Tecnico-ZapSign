from django.test import TestCase

from documentapp.external_models.doc_api_fake import DocAPIFake
from documentapp.models import Company, Document, Signer
from documentapp.usecases.create_document import CreateDocument
from documentapp.usecases.get_docs import GetDocs


class CreateDocumentTestCase(TestCase):
    def setUp(self):
        Company.objects.create(name='Company Name', api_token="''")
        doc_api = DocAPIFake()
        self.create_document = CreateDocument(doc_api)
        self.get_docs = GetDocs()

    def test_create_doc(self):
        input_data = {
            "name": "Documento A",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [
                {"name": "Signatario A", "email": "signatarioA@email.com"},
                {"name": "Signatario B", "email": "signatarioB@email.com"}
            ]
        }
        response = self.create_document.execute(input_data)
        doc = Document.objects.first()
        signer_a = Signer.objects.get(email='signatarioA@email.com')
        signer_b = Signer.objects.get(email='signatarioB@email.com')
        self.assertEqual(doc.name, "Documento A")
        self.assertEqual(signer_a.email, 'signatarioA@email.com')
        self.assertEqual(signer_b.email, 'signatarioB@email.com')
        docs = self.get_docs.execute()
        self.assertEqual(response, docs)

    def test_doc_missing_field_name(self):
        input_data = {
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"name": "Signer Name", "email": "signer@email.com"}]
        }
        with self.assertRaises(KeyError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "'missing required field: name'")

    def test_doc_missing_field_url(self):
        input_data = {
            "name": "Doc Name",
            "signers": [{"name": "Signer Name", "email": "signer@email.com"}]
        }
        with self.assertRaises(KeyError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "'missing required field: url'")

    def test_doc_missing_field_signer(self):
        input_data = {
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
        }
        with self.assertRaises(KeyError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "'missing required field: signers'")

    def test_doc_invalid_name_type(self):
        input_data = {
            "name": 123,
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"name": "Signer Name", "email": "signer@email.com"}]
        }
        with self.assertRaises(TypeError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "name must be a string")

    def test_doc_invalid_url_type(self):
        input_data = {"name": 'Doc Name', "url": 123, "signers": [{"name": "Signer Name", "email": "signer@email.com"}]}
        with self.assertRaises(TypeError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "name must be a string")

    def test_doc_invalid_signer_type(self):
        input_data = {
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": 123
        }
        with self.assertRaises(TypeError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "name must be a list")

    def test_doc_empty_signer(self):
        input_data = {
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": []
        }
        with self.assertRaises(ValueError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "signers must have at least 1 item")

    def test_doc_missing_signer_field_name(self):
        input_data = {
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"email": "signer@email.com"}]
        }
        with self.assertRaises(KeyError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "'missing signer required field: name'")

    def test_doc_missing_signer_field_email(self):
        input_data = {
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"name": "Signer Name"}]
        }
        with self.assertRaises(KeyError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "'missing signer required field: email'")

    def test_doc_invalid_signer_name_type(self):
        input_data = {
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"name": 123, "email": "signer@email.com"}]
        }
        with self.assertRaises(TypeError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "name must be a string")

    def test_doc_invalid_signer_email_type(self):
        input_data = {
            "name": "Doc Name",
            "url": "https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf",
            "signers": [{"name": "Signer Name", "email": 123}]
        }
        with self.assertRaises(TypeError) as context: self.create_document.execute(input_data)
        self.assertEqual(str(context.exception), "name must be a string")
