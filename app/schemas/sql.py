from pydantic import BaseModel

class SQLData(BaseModel):
    query: str
