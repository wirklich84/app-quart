
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import User

async def iniciar_db():
    client = AsyncIOMotorClient('mongodb://edelacruz:sip18DNK.*@localhost:27017')
    await init_beanie(database=client.sf_encuestas_it, document_models=[User])