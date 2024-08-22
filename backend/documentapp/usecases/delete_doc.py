from documentapp.models import Document, Signer


class DeleteDoc:
    def execute(self, doc_id):
        document = Document.objects.get(id=doc_id)
        document.delete()
        return True