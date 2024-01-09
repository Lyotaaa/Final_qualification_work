import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from backend.models import User, ConfirmEmailToken, Shop, Product, Category
from rest_framework.authtoken.models import Token

new_user = {
    "email": "popova_Olga@gmail.com",
    "password": "11ff22FF33cc44CC",
    "first_name": "Виктория",
    "last_name": "Плюшкина",
    "company": "Microsoft Corporation",
    "position": "manager",
}

dict_url = {
    "register": "/api/v1/user/register",
    "confirm": "/api/v1/user/register/confirm",
    "login": "/api/v1/user/login",
    "details": "/api/v1/user/details",
    "contact": "/api/v1/user/contact",
    "shops": "/api/v1/shops",
    "categories": "/api/v1/categories",

    "products": "/api/v1/products",
    "order": "/api/v1/order",

    "update": "/api/v1/partner/update",
    "state": "/api/v1/partner/state",
    "orders": "/api/v1/partner/orders",
    "basket": "/api/v1/basket",
}


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    user = User.objects.create_user(
        email=new_user["email"],
        password=new_user["password"],
        first_name=new_user["first_name"],
        last_name=new_user["last_name"],
        company=new_user["company"],
        position=new_user["position"],
    )
    return user


@pytest.fixture
def register_user(client):
    data = {
        "email": new_user["email"],
        "password": new_user["password"],
    }
    response = client.post(dict_url["register"], data=new_user)
    return response


@pytest.fixture
def confirm_user(client, user):
    token = ConfirmEmailToken.objects.create(user_id=user.id).key
    data = {
        "email": new_user["email"],
        "token": token,
    }
    response_confirm = client.post(dict_url["confirm"], data=data)
    return response_confirm, token


@pytest.fixture
def login_user(client, user, confirm_user):
    data = {
        "email": new_user["email"],
        "password": new_user["password"],
    }
    response_login = client.post(dict_url["login"], data=data)
    return response_login


@pytest.fixture
def shop_factory():
    def factory(*args, **kwargs):
        return baker.make(Shop, *args, **kwargs)

    return factory


@pytest.fixture
def product_factory():
    def factory(*args, **kwargs):
        return baker.make(Product, *args, **kwargs)

    return factory


@pytest.fixture
def categories_factory():
    def factory(*args, **kwargs):
        return baker.make(Category, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_user_register(client):
    user_count = User.objects.count()
    user = User.objects.create_user(
        email=new_user["email"],
        password=new_user["password"],
    )
    data = {
        "email": new_user["email"],
        "password": new_user["password"],
    }
    response = client.post(dict_url["register"], data=new_user)
    # response = register_user
    user_email = User.objects.get(email=user.email).email
    assert response.status_code == 200
    assert user_email == new_user["email"]
    assert user_count == 0
    assert User.objects.count() == user_count + 1


@pytest.mark.django_db
def test_user_confirm_and_test_user_login(
        client, user, register_user, confirm_user, login_user
):
    # token = ConfirmEmailToken.objects.create(user_id=user.id).key
    # data = {
    #     "email": new_user["email"],
    #     "password": new_user["password"],
    #     "token": token,
    #     "is_active": True,
    # }
    # response_confirm = client.post(dict_url["confirm"], data=data)
    # response_login = client.post(dict_url["login"], data=data)
    response_confirm, token = confirm_user[0], confirm_user[1]
    response_login = login_user
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
def test_user_details_post_and_get(
        client, user, register_user, confirm_user, login_user
):
    data = {
        "id": User.objects.get().id,
        "email": "vatrushkina_Olga@gmail.com",
        "first_name": "Ольга",
        "last_name": "Ватрушкина",
        "company": "Google",
        "position": "clerck",
        "contacts": [],
    }
    client.force_authenticate(user)
    response_post = client.post(dict_url["details"], data=data)
    response_get = client.get(dict_url["details"])
    data_post = response_post.json()
    data_get = response_get.json()
    assert response_post.status_code == 200
    assert data_post["Status"] == True
    assert data_get == data


@pytest.mark.django_db
def test_user_contact_post_and_get(
        client, user, register_user, confirm_user, login_user
):
    data = {
        "id": 1,
        "city": "Том",
        "street": "Ленина",
        "house": "1",
        "structure": "2",
        "building": "3",
        "apartment": "4",
        "phone": "+7-999-111-22-33",
    }
    client.force_authenticate(user)
    response_post = client.post(dict_url["contact"], data=data)
    response_get = client.get(dict_url["contact"])
    data_post = response_post.json()
    data_get = response_get.json()
    assert response_post.status_code == 200
    assert data_post["Status"] == True
    assert data_get[0] == data


@pytest.mark.django_db
def test_get_shop(client, user, shop_factory):
    shop = shop_factory(_quantity=5)
    client.force_authenticate(user)
    response = client.get(dict_url["shops"])
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 5
    assert len(data["results"]) == 5
    request = []
    response = []
    for i in range(len(data["results"])):
        request.append(data["results"][i]["name"])
        response.append(list(shop)[i].name)
    assert request.sort() == response.sort()


@pytest.mark.django_db
def test_get_categories(client, user, categories_factory):
    categories = categories_factory(_quantity=5)
    client.force_authenticate(user)
    response = client.get(dict_url["categories"])
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 5
    assert len(data["results"]) == 5
    request = []
    response = []
    for i in range(len(data["results"])):
        request.append(data["results"][i]["name"])
        response.append(list(categories)[i].name)
    assert request.sort() == response.sort()


# data = {
#     "partner": 1,
#     "url": "https://github.com/Lyotaaa/Final_qualification_work/edit/main/Netology/data/shop1.yaml"
# }
