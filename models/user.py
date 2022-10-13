from pydantic import BaseModel, EmailStr
from beanie import Document, Indexed

class User(Document):
    full_name : str
    dep : str
    email : Indexed(EmailStr, unique=True)
    password : str
    is_admin : bool = False

    class Collection:
        name = "users"

    class Config:
        schema_extra = {
            "ejemplo" : {
                "full_name" : " Juan Perez",
                "email" : "juan@solucionfactible.com",
                "password" : "shjb%&123"
            }
        }

class UserData(BaseModel):
    full_name: str
    email : EmailStr

    class Config:
        schema_extra = {
            "ejemplo" : {
                "full_name" : " Juan Perez",
                "email" : "juan@solucionfactible.com"         
            }
        }
        
class UserLogin(BaseModel):
    email : EmailStr
    dep : str
    password : str
    
    class Config:
        schema_extra = {
            "ejemplo" : {                
                "email" : "juan@solucionfactible.com",
                "password"  : "sjk23#$s"
            }
        }

class UserAdminView(BaseModel):
    full_name: str
    is_admin: bool
