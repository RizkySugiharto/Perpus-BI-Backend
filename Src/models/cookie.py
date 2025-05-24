from typing import Optional
from pydantic import BaseModel

class AuthCookie(BaseModel):
    token: Optional[str] = None