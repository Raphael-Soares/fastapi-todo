from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.schemas import UserDB, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_wity_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_wity_id)
    return user_wity_id
