from django.test import TestCase
from ..models import Signer
from ..usecases.update_signer import UpdateSigner


class UpdateSignerTestCase(TestCase):
    def setUp(self):
        self.signer = Signer.objects.create(
            name="Old Name",
            email="old@example.com",
            status="pending"
        )
        self.update_signer_service = UpdateSigner()

    def test_update_signer(self):
        result = self.update_signer_service.execute(self.signer.id, {'name': 'New Name'})
        self.assertTrue(result)
        self.signer.refresh_from_db()
        self.assertEqual(self.signer.name, 'New Name')

    def test_update_signer_invalid_name(self):
        with self.assertRaises(TypeError):
            self.update_signer_service.execute(self.signer.id, {'name': 123})

    def test_update_non_existent_signer(self):
        with self.assertRaises(Signer.DoesNotExist):
            self.update_signer_service.execute(99160499, {'name': 'Name'})
