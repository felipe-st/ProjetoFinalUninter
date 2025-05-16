from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta

from core.configs import settings

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.paciente_model import PacienteModel
from core.security import verificar_senha

from pydantic import EmailStr


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/pacientes/login"
)


async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[PacienteModel]:
    async with db as session:
        query = select(PacienteModel).filter(PacienteModel.email == email)
        result = await session.execute(query)
        paciente: PacienteModel = result.scalars().unique().one_or_none()

        if not paciente:
            return None

        if not verificar_senha(senha, paciente.senha):
            return None

        return paciente


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    payload = {}
    sp = timezone('America/Sao_Paulo')
    expira = datetime.now (tz=sp) + tempo_vida

    payload["type"] = tipo_token

    payload["exp"] = expira

    payload["iat"] = datetime.now(tz=sp)

    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def criar_token_acesso(sub: str) -> str:
    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
