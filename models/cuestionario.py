from sqlite3 import DataError
from pydantic import  BaseModel 
from beanie import Document
from datetime import datetime

class FortalecimientoSegudadInfo(Document):
    fecha_realizado : datetime = datetime.now()
    usuario_id : str
    pregunta_1 : str
    pregunta_2 : str
    pregunta_3 : str
    pregunta_4 : str
    pregunta_5 : str

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