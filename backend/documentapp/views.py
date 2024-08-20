import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import requests
from django.views.decorators.http import require_http_methods

from .models import Document, Signer, Company


@csrf_exempt
@require_http_methods(["POST"])
def create_document(request):
    request_data = json.loads(request.body)
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


@csrf_exempt
@require_http_methods(["GET"])
def get_documents(request):
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
    # `safe=False`: permite retornar qualquer tipo de objeto serializável em JSON, como listas, além de dicionários
    return JsonResponse(documents_list, safe=False)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_document(request, document_id):
    try:
        document = Document.objects.get(id=document_id)
        document.delete()
        return JsonResponse({'status': 'Document deleted successfully'})
    except Document.DoesNotExist:
        return HttpResponseNotFound({'status': 'Document not found'})


@csrf_exempt
@require_http_methods(["PATCH"])
def update_signer(request, signer_id):
    try:
        signer = Signer.objects.get(id=signer_id)
        data = json.loads(request.body)
        signer.name = data.get('name', signer.name)
        signer.email = data.get('email', signer.email)
        signer.save()
        return JsonResponse({'status': 'Signer updated successfully'})
    except Signer.DoesNotExist:
        return HttpResponseNotFound({'status': 'Signer not found'})
    except json.JSONDecodeError:
        return HttpResponseBadRequest({'status': 'Invalid JSON'})


@csrf_exempt
@require_http_methods(["PATCH"])
def update_document(request, document_id):
    try:
        document = Document.objects.get(id=document_id)
        data = json.loads(request.body)
        document.name = data.get('name', document.name)
        document.save()
        return JsonResponse({'status': 'Document updated successfully'})
    except Document.DoesNotExist:
        return HttpResponseNotFound({'status': 'Document not found'})
    except json.JSONDecodeError:
        return HttpResponseBadRequest({'status': 'Invalid JSON'})
