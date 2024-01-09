import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from backend.models import User, ConfirmEmailToken
from rest_framework.authtoken.models import Token

new_user = {
    "email": "popova_Olga@gmail.com",
    "password": "11ff22FF33cc44CC",
}

dict_url = {
    "update": "/api/v1/partner/update",
    "state": "/api/v1/partner/state",
    "orders": "/api/v1/partner/orders",
    "register": "/api/v1/user/register",
    "confirm": "/api/v1/user/register/confirm",
    "details": "/api/v1/user/details",
    "contact": "/api/v1/user/contact",
    "login": "/api/v1/user/login",
    "categories": "/api/v1/categories",
    "shops": "/api/v1/shops",
    "products": "/api/v1/products",
    "basket": "/api/v1/basket",
    "order": "/api/v1/order",
}


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    user = User.objects.create_user(
        email=new_user["email"],
        password=new_user["password"],
    )
    return user


@pytest.mark.django_db
def test_user_register(client):
    user_count = User.objects.count()
    assert user_count == 0
    user = User.objects.create_user(
        email=new_user["email"],
        password=new_user["password"],
    )
    data = {
        "first_name": "Ольга",
        "last_name": "Попова",
        "email": new_user["email"],
        "password": new_user["password"],
        "username": "hatz",
        "company": "Microsoft",
        "position": "manager",
    }
    response = client.post(dict_url["register"], data=new_user)
    user_email = User.objects.get(email=user.email).email
    assert response.status_code == 200
    assert user_email == new_user["email"]
    assert User.objects.count() == user_count + 1


@pytest.mark.django_db
def test_user_register_confirm_and_test_user_login(client, user):
    token = ConfirmEmailToken.objects.create(user_id=user.id).key
    data = {
        "email": new_user["email"],
        "password": new_user["password"],
        "token": token,
        "is_active": True,
    }
    response_confirm = client.post(dict_url["confirm"], data=data)
    response_login = client.post(dict_url["login"], data=data)
    user_email = User.objects.get(email=user.email).email
    user_token = Token.objects.get(user=user).key
    data_confirm = response_confirm.json()
    data_login = response_login.json()
    assert response_confirm.status_code == 200
    assert user_email == new_user["email"]
    assert token == data_confirm["token"]
    assert response_login.status_code == 200
    assert data_login["Status"] == True
    assert data_login["Token"] == user_token


@pytest.mark.django_db
def test_user_details_post_and_get(client, user):
    data = {}
    response = client.post(dict_url["details"], data=data)
