import base64

from pydantic import BaseModel, ValidationError, PydanticTypeError
from pydantic.typing import CallableGenerator
from pydantic.utils import *


class Base64Bytes(bytes):
    @classmethod
    def encode(cls, data: bytes) -> 'Base64Bytes':
        return Base64Bytes(base64.b64encode(data))

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        # yield cls.
        pass