#Este archivo tendra la estructura del Json
############################################################
from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id:Optional[int]
    name: str
    username: str
    user_passw: str

class userCredenciales(BaseModel):
    username:str
    user_passw:str