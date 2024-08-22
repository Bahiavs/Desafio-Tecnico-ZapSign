from documentapp.models import Document, Signer


class UpdateDoc:
    def execute(self, document_id, doc_data):
        doc = Document.objects.get(id=document_id)
        name = doc_data.get('name', doc.name)
        if not isinstance(name, str): raise TypeError("name field must be a string")
        doc.name = name
        doc.save()
        return True
