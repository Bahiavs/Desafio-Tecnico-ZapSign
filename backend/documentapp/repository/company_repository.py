from abc import ABC, abstractmethod

from documentapp.models import Company

class CompanyRepository(ABC):
    @abstractmethod
    def get(self) -> Company:
        pass

class CompanyRepositoryDatabase(CompanyRepository):
    def get(self) -> Company:
        company = Company.objects.first()
        if company is None: raise ValueError('Company must have a row')
        return company