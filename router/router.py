#Este archivo tendra todas las rutas y  APIs de mi APP
############################################################
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED
from schema.user_schema import UserSchema
from config.db import engine
from model.users import users
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
import json


user = APIRouter()

@user.get("/")
def root():
    return {"message": "Hi, I am API whith router"}


@user.get("/api/user", response_model=List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        # json_objeto: UserSchema = json.dumps([dict(zip(('id', 'name', 'username', 'user_passw'), registro)) for registro in result])

        return json.loads(json.dumps([dict(zip(('id', 'name', 'username', 'user_passw'), registro)) for registro in result]))

#1:03:30
@user.get("/api/user/{user_is}", response_model=UserSchema)
def get_user(user_is: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_is)).first()

        return {"id" : result[0],"name":result[1],"username":result[2],"user_passw":result[3]}


@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)
        conn.execute(users.insert().values(new_user))
        conn.commit()
        return Response(status_code=HTTP_201_CREATED)



@user.put("/api/user")
def update_user():
    pass