from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRECT_KEY, create_access_token


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(token, SECRECT_KEY, algorithms=ALGORITHM)

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer token-invalido'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials.'}
