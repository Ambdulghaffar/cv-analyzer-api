from pydantic import BaseModel

class LetterResult(BaseModel):
    content: str
