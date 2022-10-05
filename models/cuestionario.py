from sqlite3 import DataError
from pydantic import  BaseModel 
from beanie import Document
from datetime import datetime

class FortalecimientoSegudadInfo(Document):
    fecha_realizado : datetime = datetime.now()
    usuario_id : str
    pregunta_1 : int
    pregunta_2 : int
    pregunta_3 : int
    pregunta_4 : int
    pregunta_5 : int

    class Collection:
        name = "fortalecimiento_sgi"

    class Config:
        schema_extra = {
            "ejemplo" : {
                "fecha_realizado" : datetime.now(),
                "usuario_id" : "349839483948",
                "pregunta_1" : "1",
                "pregunta_2" : "3",
                "pregunta_3" : "2",
                "pregunta_4" : "1",
                "pregunta_5" : "4",
            }
        }