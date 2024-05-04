from pydantic import BaseModel
from typing import Optional

class Meme(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    image_url: str
