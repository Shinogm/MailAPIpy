from pydantic import BaseModel
from fastapi import Form
from typing import Annotated

class CreateFolder(BaseModel):
    name : str

    @classmethod
    def as_form(
            cls,
            name: Annotated[str, Form(...)]
        ):
        return cls(
            name=name
        )

class UpdateFolder(BaseModel):
    name : str | None = None

    @classmethod
    def as_form(
            cls,
            name: Annotated[str | None, Form(...)] = None
        ):
        return cls(
            name=name
        )

class UserInFolder(BaseModel):
    user_id : int
    folder_id : int

    @classmethod
    def as_form(
            cls,
            user_id: Annotated[int, Form(...)],
            folder_id: Annotated[int, Form(...)]

        ):
        return cls(
            user_id=user_id,
            folder_id=folder_id
        )

class ContactsInUserFolder(BaseModel):
    contact_id : int
    user_id : int
    folder_id : int

    @classmethod
    def as_form(
            cls,
            contact_id: Annotated[int, Form(...)],
            user_id: Annotated[int, Form(...)],
            folder_id: Annotated[int, Form(...)]

        ):
        return cls(
            contact_id=contact_id,
            user_id=user_id,
            folder_id=folder_id
        )