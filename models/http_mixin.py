from tools import token_conf

from typing import Dict
from pydantic import BaseModel


class HttpRequestMixin(BaseModel):
    base_url: str = "https://api.hh.ru/"
    user_agent: str = "Автоматизация для рекрутёров"
    access_token: str = token_conf.access_token
    token_type: str = token_conf.token_type.capitalize()

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"{self.token_type} {self.access_token}",
            "HH-User-Agent": self.user_agent,
        }
