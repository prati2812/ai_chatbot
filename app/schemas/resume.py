from pydantic import BaseModel

class ResumeData(BaseModel):
    content: str
