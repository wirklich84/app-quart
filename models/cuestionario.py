from beanie import Document, PydanticObjectId, UnionDoc
from datetime import datetime
from pydantic import BaseModel

class UserData(BaseModel):
    user_id : PydanticObjectId
    name: str
    email: str
    dep : str


class Cuestionarios(UnionDoc):
    class Settings:
        name = "cuestionarios_collection"
    

class FortalecimientoSegudadInfo(Document):
    fecha_realizado : datetime 
    user_info : UserData
    pregunta_1 : str
    pregunta_2 : str
    pregunta_3 : str
    pregunta_4 : str
    pregunta_5 : str
    codigo : str = "FO-OR-019 - Fortalecimiento"

    class Settings:
        union_doc = Cuestionarios

    '''
    class Collection:
        name = "fortalecimiento_sgi"
    '''
    




class LineamientoSeguridadInfo(Document):
    fecha_realizado : datetime
    user_info : UserData
    pregunta_1 : str
    pregunta_2 : str
    pregunta_3 : str
    pregunta_4 : str
    pregunta_5 : str
    codigo : str = "FO-OR-018 - Lineamientos"

    class Settings:
        union_doc = Cuestionarios

    '''

    class Collection:
        name = "lineamiento_sgi"
    
    '''
    