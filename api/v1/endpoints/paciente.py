from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.paciente_model import PacienteModel
from schemas.paciente_schema import PacienteSchemaBase, PacienteSchemaCreate, PacienteSchemaUpdate
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso


router = APIRouter()

#GET Logado
@router.get('/logado', response_model=PacienteSchemaBase)
def get_logado(paciente_logado: PacienteModel = Depends(get_current_user)):
    return paciente_logado

# POST / Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=PacienteSchemaBase)
async def post_paciente(paciente: PacienteSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_paciente: PacienteModel = PacienteModel(nome=paciente.nome, telefone=paciente.telefone, cpf=paciente.telefone,
                                                 idade=paciente.idade, sexo=paciente.sexo, email=paciente.email,
                                                 senha=gerar_hash_senha(paciente.senha))
    async with db as session:
        session.add(novo_paciente)
        await session.commit()

        return novo_paciente


# GET Usuarios
@router.get('/', response_model=List[PacienteSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PacienteModel)
        result = await session.execute(query)
        pacientes: List[PacienteSchemaBase] = result.scalars().unique().all

        return pacientes


# GET Usuario
@router.get('/{paciente_id}', response_model=PacienteSchemaBase, status_code=status.HTTP_200_OK)
async def get_paciente(paciente_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PacienteModel).filter(PacienteModel.id==paciente_id)
        result = await session.execute(query)
        paciente: PacienteSchemaBase = result.scalars().unique().one_or_none
        if paciente:
            return paciente
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


# PUT Paciente
@router.put('/{paciente_id}', response_model=PacienteSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_paciente(paciente_id: int, paciente: PacienteSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PacienteModel).filter(PacienteModel.id==paciente_id)
        result = await session.execute(query)
        paciente_update: PacienteSchemaBase = result.scalars().unique().one_or_none
        if paciente_update:
            if paciente.nome:
                paciente_update.nome = paciente.nome
            if paciente.telefone:
                paciente_update.telefone = paciente.telefone
            if paciente.cpf:
                paciente_update.cpf = paciente.cpf
            if paciente.idade:
                paciente_update.idade = paciente.idade
            if paciente.sexo:
                paciente_update.sexo = paciente.sexo
            if paciente.email:
                paciente_update.email = paciente.email
            if paciente.senha:
                paciente_update.senha = gerar_hash_senha(paciente.senha)

            await session.commit()

            return paciente_update
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


# DELETE Usuario
@router.delete('/{paciente_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_paciente(paciente_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PacienteModel).filter(PacienteModel.id==paciente_id)
        result = await session.execute(query)
        paciente_delete: PacienteSchemaBase = result.scalars().unique().one_or_none
        if paciente_delete:
            await session.delete(paciente_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)



# POST Login
@router.post('/loginm')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    paciente = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not paciente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos.')

    return  JSONResponse(content={"acess_token": criar_token_acesso(sub=paciente.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)