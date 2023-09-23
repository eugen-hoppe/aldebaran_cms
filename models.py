from typing import Any

from fastapi import Request
from pydantic import BaseModel

from settings import constants, options


class Data(BaseModel):
    website: options.Website = options.Website()
    payload: dict[str, Any] = dict()

    def context(self, request: Request) -> dict[str, Any]:
        output = {**{"request": request}, **self.website.__dict__}
        return {**output, **self.payload}
    
    @staticmethod
    def template():
        return constants.Template.BASE.value + ".html"
