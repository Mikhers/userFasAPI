#Este archivo tendra todas las rutas y  APIs de mi APP
############################################################
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user_schema import UserSchema,userCredenciales
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
@user.get("/api/user/{user_id}", response_model=UserSchema)
def get_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()

        return {"id" : result[0],"name":result[1],"username":result[2],"user_passw":result[3]}


@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)
        conn.execute(users.insert().values(new_user))
        conn.commit()
        return Response(status_code=HTTP_201_CREATED)



@user.put("/api/user/{user_id}", response_model=UserSchema)
def update_user(data_update: UserSchema, user_id: str):
    with engine.connect() as conn:
        encry_pss = generate_password_hash(data_update.user_passw, "pbkdf2:sha256:30", 20)
        conn.execute(users.update()
        .values(name=data_update.name, username=data_update.username, user_passw=encry_pss)
        .where(users.c.id == user_id))
        conn.commit()

        result = conn.execute(users.select().where(users.c.id == user_id)).first()

        return {"id" : result[0],"name":result[1],"username":result[2],"user_passw":result[3]}


@user.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)#, response_model=UserSchema
def update_user(user_id: str):
    with engine.connect() as conn:
        conn.execute(users.delete()
        .where(users.c.id == user_id))
        conn.commit()

        return Response(status_code=HTTP_204_NO_CONTENT)

#1:25:04
@user.post("/api/user/login", status_code=200)
def user_login(credentiales: userCredenciales):
    with engine.connect()as conn:
        result = conn.execute(users.select().where(
            users.c.username==credentiales.username)).first()

        if result != None:
            check = check_password_hash(result[3],credentiales.user_passw)

            if check:
                return {"status":200,"name":result[1],"username":result[2]}
        return {"status": HTTP_401_UNAUTHORIZED, }