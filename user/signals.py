from django.contrib.auth.hashers import identify_hasher
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import identify_hasher


@receiver(pre_save, sender=get_user_model())
def hash_password(sender, instance, **kwargs):
    try:
        identify_hasher(instance.password)
    except:
        if instance._state.adding and not instance.pk:
            # Если это создание нового пользователя, хешируем пароль
            instance.set_password(instance.password)
        elif not instance._state.adding:
            # Если это обновление существующего пользователя, проверяем, изменился ли пароль
            original = sender.objects.get(pk=instance.pk)
            if instance.password != original.password:
                # Пароль изменился, хешируем его
                instance.set_password(instance.password)
