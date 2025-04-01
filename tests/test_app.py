from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.models import User
from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'password': 'passwd',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'test',
        'email': 'test@test.com',
        'id': 1,
    }


def test_create_user_with_existing_email(client, user: User):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'password': 'passwd',
            'email': user.email,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user_with_existing_username(client, user: User):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'password': user.password,
            'email': 'test_create_user_with_existing_username@mail.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_user(client: TestClient, user: User):
    response = client.get('/users/{user_id}'.format(user_id=user.id))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_users_with_user(client: TestClient, user: User):
    response = client.get('/users/')
    user_chema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_chema]}


def test_read_users(client: TestClient):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_update_user(client, user: User):
    user_public: UserPublic = UserPublic.model_validate(user)
    user_public.model_dump()

    response = client.put(
        '/users/{user_id}'.format(user_id=user.id),
        json={
            'password': user.password,
            'username': user.username,
            'email': 'updated@test.com',
            'id': user.id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': 'updated@test.com',
        'id': user.id,
    }


def test_delete_user(client, user: User):
    response = client.delete('/users/{user_id}'.format(user_id=user.id))
    assert response.json() == {'message': 'User deleted'}


def test_not_found_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_not_found_update_user(client):
    response = client.put(
        '/users/999999999999999',
        json={
            'password': 'passwd',
            'username': 'updated user',
            'email': 'updated@test.com',
            'id': 9999999,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
