from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Signer:
    external_id: str
    token: str
    status: str


@dataclass
class CreateDocAPIRes:
    external_id: str
    open_id: int
    token: str
    status: str
    created_by_email: str
    signers: List[Signer]


class DocAPI(ABC):
    @abstractmethod
    def create_doc(self, data) -> str | CreateDocAPIRes: pass
