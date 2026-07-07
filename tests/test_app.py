from http import HTTPStatus

from viajei_api.schemas.user import UserPublic


def test_root(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"funcionou": "(/◕ヮ◕)/"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "jorge@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "email": "jorge@example.com",
        "id": 1,
    }


def test_read_user(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_user_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.json() == {"users": [user_schema]}


def test_delete_user(client, user):

    response = client.delete("/users/1")

    response.status_code == HTTPStatus.OK
    response.json() == {"message": "User deleted"}


def test_delete_notfound(client):

    response = client.delete("/users/0")

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"message": "User not found"}


def test_get_notfound(client):

    response = client.get("/users/0")

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"detail": "User not found"}


def test_get_200(client):

    response = client.get("/users/1")

    response.status_code == HTTPStatus.OK
    response.json() == {
        "email": "jorge@example.com",
        "id": 1,
    }


def test_get_token(client, user):
    response = client.post(
        "/auth",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


def test_create_story(authenticated_user):

    response = authenticated_user.post(
        "/story",
        json={
            "author": "Fulaninho",
            "title": "Pensando ilimitado",
            "story": "Que baita história",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "title": "Pensando ilimitado",
        "email": "jorge@example.com",
    }
