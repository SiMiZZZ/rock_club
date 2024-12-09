from typing import Self

from blacksheep import FormPart
from pydantic import BaseModel


class File(BaseModel):
    filename: str
    data: bytes

    @property
    def file_extension(self) -> str:
        extension = self.filename.split(".")[-1]
        return f".{extension}" if extension else ""

    @classmethod
    def from_form_part(cls, form_part: FormPart) -> Self:
        return cls(
            filename=form_part.file_name,
            data=form_part.data,
        )
