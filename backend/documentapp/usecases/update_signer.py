from documentapp.models import Signer


class UpdateSigner:
    def execute(self, signer_id, signer_data):
        signer = Signer.objects.get(id=signer_id)
        name = signer_data.get('name', signer.name)
        if not isinstance(name, str): raise TypeError("name field must be a string")
        signer.name = name
        signer.save()
        return True