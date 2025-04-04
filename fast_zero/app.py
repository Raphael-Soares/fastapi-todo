from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)) -> UserPublic:
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists.',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists.',
            )

    db_user = User(
        email=user.email,
        password=user.password,
        username=user.username,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return UserPublic(
        email=db_user.email, username=db_user.username, id=db_user.id
    )


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    users = session.scalars(select(User).limit(limit).offset(offset)).all()
    return {'users': users}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))
    return user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    db_user.email = user.email
    db_user.password = user.password
    db_user.username = user.username

    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found.'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
