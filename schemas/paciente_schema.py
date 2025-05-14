from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr


class PacienteSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: str
    cpf: str
    idade: str
    sexo: str
    email: EmailStr

    class Config:
        orm_mode = True


class PacienteSchemaCreate(PacienteSchemaBase):
    senha = str


class PacienteSchemaUpdate(PacienteSchemaBase):
    nome: Optional[str]
    telefone = Optional[str]
    cpf = Optional[str]
    idade = Optional[str]
    sexo = Optional[str]
    email = Optional[EmailStr]
    senha = Optional[str]
