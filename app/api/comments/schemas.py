from pydantic import BaseModel

class CommentCreateRequest(BaseModel):
    text: str