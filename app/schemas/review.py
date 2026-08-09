from pydantic import BaseModel

class ReviewData(BaseModel):
    feedback: str
