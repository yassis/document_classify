from pydantic import BaseModel
from typing import Optional, List, Dict

# request models

class SingleTextQuery(BaseModel):
    document_text: str

class MultipleTextQuery(BaseModel):
    texts: List[str]


class APIInfo(BaseModel):
    api_name: str
    astra_db_keyspace: str
    caller_id: str
    model_directory: str
    model_version: str
    started_at: str


class PredictionTopInfo(BaseModel):
    label: str
    value: float


class PredictionResult(BaseModel):
    prediction: Dict[str, float]
    top: PredictionTopInfo
    message: Optional[str]

