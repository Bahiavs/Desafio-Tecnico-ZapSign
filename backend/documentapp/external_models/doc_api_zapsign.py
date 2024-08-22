import requests
from documentapp.external_models.doc_api import DocAPI, CreateDocAPIRes, Signer


class DocAPIZapSign(DocAPI):
    def __init__(self, api_token, api_url):
        self.api_token = api_token
        self.api_url = api_url

    def create_doc(self, data) -> str | CreateDocAPIRes:
        headers = {'Authorization': f'Bearer {self.api_token}'}
        response = requests.post(
            self.api_url,
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
