from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class PacienteModel(settings.DBBaseModel):
    __tablename__ = 'pacientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256))
    telefone = Column(String(20))
    cpf = Column(String(20))
    idade = Column(String(3))
    sexo =Column(String(1))
    email = Column(String(256), index=True, nullable=False, unique=True)
    senha = Column(String(256), nullable=False)
