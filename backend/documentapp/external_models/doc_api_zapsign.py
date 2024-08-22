import requests
from documentapp.external_models.doc_api import DocAPI, CreateDocAPIRes, Signer


class DocAPIZapSign(DocAPI):
    def __init__(self, api_token):
        self.api_token = api_token

    def create_doc(self, data) -> str | CreateDocAPIRes:
        headers = {'Authorization': f'Bearer {self.api_token}'}  # todo - obter Token do env
        response = requests.post(
            'https://sandbox.api.zapsign.com.br/api/v1/docs/', # todo - obter URL do env
            json=data,
            headers=headers
        )
        if response.status_code != 200: return f"Error: {response.status_code}"
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