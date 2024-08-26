import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from backend import settings
from .external_models.doc_api_zapsign import DocAPIZapSign
from .models import Document, Signer
from .usecases.create_document import CreateDocument
from .usecases.delete_doc import DeleteDoc
from .usecases.get_docs import GetDocs
from .usecases.update_doc import UpdateDoc
from .usecases.update_signer import UpdateSigner


@csrf_exempt
@require_http_methods(["POST"])
def create_document(request):
    try:
        doc_api = DocAPIZapSign(settings.ZAPSIGN_API_URL)
        create_doc = CreateDocument(doc_api)
        input_data = json.loads(request.body)
        docs = create_doc.execute(input_data)
        return JsonResponse(docs, safe=False, status=200)
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
        return JsonResponse({'success': 'signer updated'}, status=200)
    except Signer.DoesNotExist:
        return HttpResponseNotFound({'error': 'signer not found'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["PATCH"])
def update_document(request, document_id):
    try:
        doc_data = json.loads(request.body)
        UpdateDoc().execute(document_id, doc_data)
        return JsonResponse({'success': 'document updated'}, status=200)
    except Document.DoesNotExist:
        return HttpResponseNotFound({'error': 'document not found'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
