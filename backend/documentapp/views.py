from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Document, Signer, Company


@csrf_exempt
def create_document(request):
    company = Company.objects.first()
    data = {
        'name': 'Nome do contrato PDF',
        'signers': [{'name': 'Vinicius Signatário', 'email': 'vini.bahiarj@gmail.com'}],
        'url_pdf': 'https://zapsign.s3.amazonaws.com/2022/1/pdf/63d19807-cbfa-4b51-8571-215ad0f4eb98/ca42e7be-c932-482c-b70b-92ad7aea04be.pdf',
    }
    headers = {
        'Authorization': f'Bearer {company.api_token}'
    }
    response = requests.post('https://sandbox.api.zapsign.com.br/api/v1/docs/', json=data, headers=headers)
    if response.status_code == 200:
        return JsonResponse(response.json())
    return JsonResponse({'error': 'Error creating document'})
