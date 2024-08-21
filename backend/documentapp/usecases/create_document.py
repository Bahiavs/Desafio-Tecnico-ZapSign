import json
from django.http import JsonResponse
from ..models import Document, Signer, Company
from ..interface_adapters.doc_api.doc_api import DocAPI, CreateDocAPIRes


class CreateDocument:
    def __init__(self, doc_api: DocAPI):
        self.doc_api = doc_api

    def execute(self, input_data):
        request_data = json.loads(input_data)

        required_doc_fields = ['name', 'url', 'signers']
        required_signer_fields = ['name', 'email']
        for field in required_doc_fields:
            if field not in request_data:
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
        if not isinstance(request_data['name'], str):
            return JsonResponse({'error': 'name must be a string'}, status=400)
        if not isinstance(request_data['url'], str):
            return JsonResponse({'error': 'url must be a string'}, status=400)
        if not isinstance(request_data['signers'], list):
            return JsonResponse({'error': 'signers must be a list'}, status=400)
        if len(request_data['signers']) == 0:
            return JsonResponse({'error': 'signers must have at least 1 item'}, status=400)
        for signer in request_data['signers']:
            for field in required_signer_fields:
                if field not in signer:
                    return JsonResponse({'error': f'Missing required field in a signer: {field}'}, status=400)
        for signer in request_data['signers']:
            if not isinstance(signer['name'], str):
                return JsonResponse({'error': 'Signer name must be a string'}, status=400)
            if not isinstance(signer['email'], str):
                return JsonResponse({'error': 'Signer email must be a string'}, status=400)

        company = Company.objects.first()
        document = Document.objects.create(companyID=company, name=request_data['name'], status='initial')
        signers_data = request_data['signers']
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
            'url_pdf': request_data['url'],
        }
        response = self.doc_api.create_doc(data)
        if isinstance(response, CreateDocAPIRes):
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
            return JsonResponse({'status': 'Document created successfully'})
        return JsonResponse({'status': 'Error creating document', 'error': response.text}, status=400)
