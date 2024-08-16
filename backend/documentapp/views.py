import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Document, Signer, Company


@csrf_exempt
def create_document(request):
    request_data = json.loads(request.body)
    company = Company.objects.first()
    document = Document.objects.create(
        companyID=company,
        name=request_data['name'],
        status='initial'
    )
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
        document.save()
        for signer, signer_data in zip(signers, document_data['signers']):
            signer.externalID = signer_data['external_id']
            signer.token = signer_data['token']
            signer.status = signer_data['status']
            signer.save()
        return JsonResponse({'status': 'Document created successfully'})
    return JsonResponse({'status': 'Error creating document', 'error': response.text}, status=400)
