from .get_docs import GetDocs
from ..models import Document, Signer, Company
from ..external_models.doc_api import DocAPI


class CreateDocument:
    def __init__(self, doc_api: DocAPI):
        self.doc_api = doc_api
        self.get_docs = GetDocs()

    def execute(self, input_data):
        required_doc_fields = ['name', 'url', 'signers']
        required_signer_fields = ['name', 'email']
        for field in required_doc_fields:
            if field not in input_data: raise KeyError(f'missing required field: {field}')
        if not isinstance(input_data['name'], str): raise TypeError('name must be a string')
        if not isinstance(input_data['url'], str): raise TypeError('name must be a string')
        if not isinstance(input_data['signers'], list): raise TypeError('name must be a list')
        if len(input_data['signers']) == 0: raise ValueError('signers must have at least 1 item')
        for signer in input_data['signers']:
            for field in required_signer_fields:
                if field not in signer: raise KeyError(f'missing signer required field: {field}')
        for signer in input_data['signers']:
            if not isinstance(signer['name'], str): raise TypeError('name must be a string')
            if not isinstance(signer['email'], str): raise TypeError('name must be a string')
        company = Company.objects.first()
        document = Document.objects.create(companyID=company, name=input_data['name'], status='initial')
        signers_data = input_data['signers']
        signers = []
        for signer in signers_data:
            signer_obj = Signer.objects.create(
                documentID=document,
                name=signer['name'],
                email=signer['email'],
                status='pending'
            )
            signers.append(signer_obj)
        data = {
            'name': document.name,
            'signers': [{'name': signer.name, 'email': signer.email} for signer in signers],
            'url_pdf': input_data['url'],
        }
        response = self.doc_api.create_doc(data)
        document.openID = response.open_id
        document.externalID = response.external_id
        document.token = response.token
        document.status = response.status
        document.created_by = response.created_by_email
        document.save()
        for signer, signer_data in zip(signers, response.signers):
            signer.externalID = signer_data.external_id
            signer.token = signer_data.token
            signer.status = signer_data.status
            signer.save()
        return self.get_docs.execute()
