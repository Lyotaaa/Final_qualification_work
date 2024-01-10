import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from backend.models import (
    User,
    ConfirmEmailToken,
    Shop,
    Product,
    Category,
    ProductInfo,
    Parameter,
    ProductParameter,
)
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
    "update": "/api/v1/partner/update",
    "state": "/api/v1/partner/state",
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
        type="shop",
    )
    return user


@pytest.fixture
def register_user(client):
    data = {
        "email": new_user["email"],
        "password": new_user["password"],
    }
    response = client.post(dict_url["register"], data=data)
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
    def factory(**kwargs):
        category = baker.make(Category, **kwargs)
        product = baker.make(Product, category_id=category[0].id, **kwargs)
        shop = baker.make(Shop, **kwargs)
        return baker.make(
            ProductInfo, product_id=product[0].id, shop_id=shop[0].id, **kwargs
        )

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
    response = client.post(dict_url["register"], data=data)
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
    assert data_login["Status"] == 1  # True
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
    assert data_post["Status"] == 1  # True
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
    assert data_post["Status"] == 1  # True
    assert data_get[0] == data


@pytest.mark.django_db
def test_get_shop(client, user, shop_factory):
    shop = shop_factory(_quantity=3)
    client.force_authenticate(user)
    response = client.get(dict_url["shops"])
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 3
    assert len(data["results"]) == 3
    request = []
    response = []
    for i in range(len(data["results"])):
        response.append(data["results"][i]["name"])
        request.append(list(shop)[i].name)
    assert request.sort() == response.sort()


@pytest.mark.django_db
def test_get_categories(client, user, categories_factory):
    categories = categories_factory(_quantity=3)
    client.force_authenticate(user)
    response = client.get(dict_url["categories"])
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == 3
    assert len(data["results"]) == 3
    request = []
    response = []
    for i in range(len(data["results"])):
        response.append(data["results"][i]["name"])
        request.append(list(categories)[i].name)
    assert request.sort() == response.sort()


@pytest.mark.django_db
def test_get_products(client, user, product_factory):
    product_factory(_quantity=3)
    client.force_authenticate(user)
    response = client.get(dict_url["products"])
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 3


@pytest.mark.django_db
def test_partner_update_and_get_and_post_state(client, user):
    client.force_authenticate(user)
    data = {
        "partner": user.id,
        "url": "https://raw.githubusercontent.com/netology-code/pd-diplom/master/data/shop1.yaml",
    }
    response = client.post(dict_url["update"], data=data, format="json")
    response_get = client.get(dict_url["state"])
    data = {
        "id": 1,
        "name": "Связной",
        "state": "False",
    }
    response_state_update = client.post(dict_url["state"], data=data)
    client.force_authenticate(user=None)
    data = response_get.json()
    data_get_post = response_state_update.json()
    assert response.status_code == 200
    assert Shop.objects.count() == 1
    assert Category.objects.count() == 3
    assert Product.objects.count() == 4
    assert ProductInfo.objects.count() == 4
    assert Parameter.objects.count() == 4
    assert ProductParameter.objects.count() == 16
    assert response_get.status_code == 200
    assert data["state"] == 1
    assert response_state_update.status_code == 200
    assert data_get_post["Status"] == 1  # True

