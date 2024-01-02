from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created
from backend.models import ConfirmEmailToken, User

new_user_registered = Signal(
    providing_args=["user_id"],
)

new_order = Signal(
    providing_args=["user_id"],
)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    # Отправляем письмо с токеном для сброса пароля
    # Когда токен создан, пользователю необходимо отправить электронное письмо
    # Параметр sender: Класс представления, отправивший сигнал
    # Параметр instance: Экземпляр представления, отправивший сигнал
    # Параметр reset_password_token: Объект модели токена
    # Параметр kwargs:
    # Вернуть:
    # Отправить электронное письмо пользователю
    msg = EmailMultiAlternatives(
        # title:
        f"Токен сброса пароля для {reset_password_token.user}",
        # message:
        reset_password_token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email],
    )
    msg.send()


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    # Отправляем письмо с подтверждением почты
    # отправить электронное письмо пользователю
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
    msg = EmailMultiAlternatives(
        # title:
        f"Токен сброса пароля для {token.user.email}",
        # message:
        token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [token.user.email],
    )
    msg.send()

@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    # Отправляем письмо при изменении статуса заказа
    # отправить электронное письмо пользователю
    user = User.objects.get(id=user_id)
    msg = EmailMultiAlternatives(
        # title:
        f"Обновление статуса заказа",
        # message:
        f"Заказ сформирован",
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email],
    )
    msg.send()