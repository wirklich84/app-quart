from beanie import Document, PydanticObjectId
from datetime import datetime
from pydantic import BaseModel

class UserData(BaseModel):
    user_id : PydanticObjectId
    name: str
    email: str
    

class FortalecimientoSegudadInfo(Document):
    fecha_realizado : datetime = datetime.now()
    user_info : UserData
    pregunta_1 : str
    pregunta_2 : str
    pregunta_3 : str
    pregunta_4 : str
    pregunta_5 : str

    class Collection:
        name = "fortalecimiento_sgi"




class LineamientoSeguridadInfo(Document):
    fecha_realizado : datetime = datetime.now()
    user_info : UserData
    pregunta_1 : str
    pregunta_2 : str
    pregunta_3 : str
    pregunta_4 : str
    pregunta_5 : str

    class Collection:
        name = "lineamiento_sgi"
    