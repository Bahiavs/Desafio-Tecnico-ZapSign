import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .interface_adapters.doc_api.doc_api_zapsign import DocAPIZapSign
from .models import Document, Signer
from .usecases.create_document import CreateDocument


@csrf_exempt
@require_http_methods(["POST"])
def create_document(request):
    try:
        doc_api = DocAPIZapSign('b55b295b-20ee-4757-a71a-7185ced23ee599b274bc-b94c-42f5-aa1d-864af1605a57') # todo - obter token pelo env var
        create_doc = CreateDocument(doc_api)
        input_data = json.loads(request.body)
        create_doc.execute(input_data)
        return JsonResponse({'success': 'document created'}, status=200)
    except Exception as e:
        error_msg = str(e).strip("'\"")
        return JsonResponse({'error': error_msg}, status=400)

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
