import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import User
from models.cuestionario import FortalecimientoSegudadInfo, LineamientoSeguridadInfo, Cuestionarios

async def iniciar_db():
    client = AsyncIOMotorClient(os.environ["DB_URL"])
    await init_beanie(database=client.sf_encuestas_it, document_models=[User, FortalecimientoSegudadInfo, LineamientoSeguridadInfo, Cuestionarios])
