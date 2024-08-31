import requests
from backend import settings
from documentapp.external_models.doc_api import DocAPI, CreateDocAPIRes, Signer
from documentapp.models import Company


class DocAPIZapSign(DocAPI):
    def create_doc(self, data) -> CreateDocAPIRes:
        company = Company.objects.get(name="ZapSign")
        api_token = company.api_token
        headers = {'Authorization': f'Bearer {api_token}'}
        response = requests.post(
            settings.ZAPSIGN_API_URL,
            json=data,
            headers=headers
        )
        if response.status_code != 200: raise RuntimeError(f"error: external API not responding correctly")
        response_body = response.json()
        signers = []
        for signer in response_body['signers']:
            signers.append(Signer(external_id=signer['external_id'], token=signer['token'], status=signer['status']))
        docs = CreateDocAPIRes(
            open_id=response_body['open_id'],
            external_id=response_body['external_id'],
            token=response_body['token'],
            status=response_body['status'],
            created_by_email=response_body['created_by']['email'],
            signers=signers,
        )
        return docs
