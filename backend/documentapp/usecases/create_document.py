import json
from django.http import JsonResponse
import requests
from ..models import Document, Signer, Company


class CreateDocument:
    def __init__(self):
        pass

    def execute(self, input_data):
        request_data = json.loads(input_data.body)

        required_doc_fields = ['name', 'url', 'signers']
        required_signer_fields = ['name', 'email']
        for field in required_doc_fields:
            if field not in request_data:
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
        if not isinstance(request_data['name'], str):
            return JsonResponse({'error': 'Name must be a string'}, status=400)
        if not isinstance(request_data['url'], str):
            return JsonResponse({'error': 'URL must be a string'}, status=400)
        if not isinstance(request_data['signers'], list):
            return JsonResponse({'error': 'Signers must be a list'}, status=400)
        if len(request_data['signers']) == 0: return JsonResponse({'error': 'Signers must at least 1 item'}, status=400)
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
        headers = {'Authorization': f'Bearer {company.api_token}'}
        response = requests.post('https://sandbox.api.zapsign.com.br/api/v1/docs/', json=data, headers=headers)
        if response.status_code == 200:
            document_data = response.json()
            document.openID = document_data['open_id']
            document.externalID = document_data['external_id']
            document.token = document_data['token']
            document.status = document_data['status']
            document.created_by = document_data['created_by']['email']
            document.save()
            for signer, signer_data in zip(signers, document_data['signers']):
                signer.externalID = signer_data['external_id']
                signer.token = signer_data['token']
                signer.status = signer_data['status']
                signer.save()
            return JsonResponse({'status': 'Document created successfully'})
        return JsonResponse({'status': 'Error creating document', 'error': response.text}, status=400)
