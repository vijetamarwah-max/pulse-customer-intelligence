from typing import Dict

from pydantic import BaseModel


class CRMContract(BaseModel):
    user_id: str
    crm_context: Dict
