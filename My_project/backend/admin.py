from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import (
    User,
    Shop,
    Category,
    Product,
    ProductInfo,
    Parameter,
    ProductParameter,
    Order,
    OrderItem,
    Contact,
    ConfirmEmailToken,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Панель управления пользователями
    model = User
    fieldsets = (
        (None, {"fields": ("email", "password", "type")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "company", "position")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    # Список магазинов
    model = Shop
    list_display = ["id", "name", "user", "state"]
    search_fields = (
        "name",
        "user__first_name",
        "user__last_name",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Список категорий
    model = Category
    list_display = ["id", "name"]
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Список продуктов
    model = Product
    list_display = ["id", "name", "category"]
    search_fields = (
        "id",
        "name",
        "category__name",
    )


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    model = ProductInfo
    list_display = [
        "id",
        "model",
        "external_id",
        "product",
        "shop",
        "quantity",
        "price",
        "price_rrc",
    ]
    search_fields = (
        "id",
        "model",
        "price",
        "price_rrc",
        "product__name",
        "shop__name",
        "quantity",
    )


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    # Список имен параметров
    pass


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    # Список параметров
    model = ProductParameter
    list_display = ["product_name", "parameter", "value"]
    search_fields = ("parameter__name", "product_name", "value")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Список контактов пользователя
    model = Contact
    list_display = (
        "id",
        "user",
        "city",
        "street",
        "house",
        "structure",
        "building",
        "apartment",
        "phone",
    )
    search_fields = (
        "id",
        "user__first_name",
        "user__last_name",
        "city",
        "street",
        "phone",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Список заказов
    model = Order
    list_display = ["id", "user", "datatime", "contact", "state"]
    search_fields = (
        "id",
        "user__first_name",
        "user__last_name",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    # Список заказанных позиций
    model = OrderItem

    list_display = [
        "id",
        "order",
        "category",
        "shop",
        "quantity",
        "product_info",
    ]
    search_fields = (
        "id",
        "category__name",
        "shop__name",
        "quantity",
    )


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    # Токены подтверждения Email
    list_display = (
        "user",
        "key",
        "created_at",
    )
