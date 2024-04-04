'''from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    # group = models.IntegerField()  # Предполагается, что это должно быть ForeignKey, если это ссылка на другую модель
    # login_field = models.CharField(max_length=50)  # Необходимо уточнить назначение этого поля
    course_bought = models.BooleanField(default=True)
    date_of_next_payment = models.DateField()
    # is_active = models.BooleanField(default=True)  # Это поле уже определено в AbstractUser, его переопределение не требуется

    def __str__(self):
        return self.username
'''