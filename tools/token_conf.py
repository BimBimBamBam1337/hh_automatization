from pathlib import Path
from pydantic import BaseModel


import json


class TokenConfig(BaseModel):
    access_token: str
    token_type: str

    @staticmethod
    def get_token(file="api_token.json"):
        data = json.loads(Path(file).read_text())
        return TokenConfig(**data)


token_conf = TokenConfig.get_token()
