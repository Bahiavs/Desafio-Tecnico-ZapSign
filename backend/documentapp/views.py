import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .interface_adapters.doc_api.doc_api_zapsign import DocAPIZapSign
from .models import Document, Signer
from .usecases.create_document import CreateDocument
from .usecases.delete_doc import DeleteDoc
from .usecases.get_docs import GetDocs
from .usecases.update_signer import UpdateSigner


@csrf_exempt
@require_http_methods(["POST"])
def create_document(request):
    try:
        doc_api = DocAPIZapSign('b55b295b-20ee-4757-a71a-7185ced23ee599b274bc-b94c-42f5-aa1d-864af1605a57')  # todo - obter token pelo env var
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
    try:
        get_doc = GetDocs()
        docs = get_doc.execute()
        return JsonResponse(docs, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_document(request, document_id):
    try:
        DeleteDoc().execute(document_id)
        return JsonResponse({'success': 'document deleted'}, status=200)
    except Document.DoesNotExist:
        return HttpResponseNotFound({'error': 'document not found'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["PATCH"])
def update_signer(request, signer_id):
    try:
        signer_data = json.loads(request.body)
        UpdateSigner().execute(signer_id, signer_data)
        return JsonResponse({'status': 'signer updated successfully'}, status=200)
    except Signer.DoesNotExist:
        return HttpResponseNotFound({'error': 'signer not found'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


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
