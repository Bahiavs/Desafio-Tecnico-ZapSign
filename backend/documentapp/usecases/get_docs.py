from documentapp.models import Document, Signer


class GetDocs:
    def execute(self):
        documents = Document.objects.all()
        documents_list = []
        for document in documents:
            signers = Signer.objects.filter(documentID=document)
            signers_list = list(signers.values('name', 'email', 'status', 'id'))
            documents_list.append({
                'documentID': document.id,
                'name': document.name,
                'status': document.status,
                'createdAt': document.created_at,
                'createdBy': document.created_by,
                'signers': signers_list
            })
        return documents_list
