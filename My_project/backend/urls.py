from django.urls import path
from django_rest_passwordreset.views import (
    reset_password_request_token,
    reset_password_confirm,
)

from backend.views import (
    PartnerUpdate,
    PartnerState,
    PartnerOrders,
    RegisterAccount,
    ConfirmAccount,
    AccountDetails,
    ContactView,
    LoginAccount,
    CategoryView,
    ShopView,
    ProductInfoView,
    BasketView,
    OrderView,
)

app_name = "backend"
urlpatterns = [
    path(
        "partner/update",
        PartnerUpdate.as_view(),
        name="Обновленная информация о партнерах",
    ),
    path("partner/state", PartnerState.as_view(), name="partner-state"),
    path("partner/orders", PartnerOrders.as_view(), name="Заказы партнеров"),
    path("user/register", RegisterAccount.as_view(), name="Регистрация пользователя"),
    path(
        "user/register/confirm",
        ConfirmAccount.as_view(),
        name="Подтверждение регистрации пользователя",
    ),
    path("user/details", AccountDetails.as_view(), name="Сведения о пользователе"),
    path("user/contact", ContactView.as_view(), name="Контакт с пользователем"),
    path("user/login", LoginAccount.as_view(), name="Вход пользователя в систему"),
    path("user/password_reset", reset_password_request_token, name="Сброс пароля"),
    path(
        "user/password_reset/confirm",
        reset_password_confirm,
        name="Подтверждение сброса пароля",
    ),
    path("categories", CategoryView.as_view(), name="Категории"),
    path("shops", ShopView.as_view(), name="Магазины"),
    path("products", ProductInfoView.as_view(), name="Продукты"),
    path("basket", BasketView.as_view(), name="Корзина"),
    path("order", OrderView.as_view(), name="Заказы"),
]
