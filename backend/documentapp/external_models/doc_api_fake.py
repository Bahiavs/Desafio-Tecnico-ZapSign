from documentapp.external_models.doc_api import DocAPI, CreateDocAPIRes, Signer


class DocAPIFake(DocAPI):
    def create_doc(self, data) -> CreateDocAPIRes:
        docs = CreateDocAPIRes(
            open_id=1,
            external_id='',
            token='',
            status='',
            created_by_email='',
            signers=[Signer(external_id='', token='', status='') for _ in data['signers']],
        )
        return docs