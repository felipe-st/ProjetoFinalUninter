from fastapi import APIRouter

from api.v1.endpoints import paciente


api_router = APIRouter()

api_router.include_router(paciente.router, prefix='/pacientes', tags=['pacientes'])
