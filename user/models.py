from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db import models


class Themes(models.Model):
    name = models.CharField('Название темы', max_length=100)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.name
class Lesson(models.Model):
    name = models.CharField('Название урокa', max_length=50)
    ref = models.CharField('Ссылка на урок', max_length=250)
    file = models.FileField('Прикрепленный файл', null=True, blank=True,)
    date = models.DateTimeField('Дата публикации')
    theme = models.ForeignKey(Themes, on_delete=models.CASCADE, verbose_name='Тема', related_name='feedbacks', null=True, blank=True)
    group = models.CharField('Группа', max_length=1)
    Description = models.TextField('Описание', null=True, blank=True,)

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super(Lesson, self).save(*args, **kwargs)
        if is_new:
            users_in_group = CustomUser.objects.filter(groups__name=self.group)
            for user in users_in_group:
                LessonFeedback.objects.create(lesson=self, user=user)
        else:
            self.feedbacks.update(
                lesson=self)


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'  # Используем email вместо username для аутентификации
    REQUIRED_FIELDS = ['username']
    PASSWORD_FIELD = 'password'
    email = models.EmailField(unique=True)
    date_of_next_payment = models.DateField(default=now)
    birth_date = models.DateField(null=True, blank=True)
    course_bought = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Schedule(models.Model):
    group = models.IntegerField(null=True, blank=True, verbose_name='Группа')
    monday = models.BooleanField(default=False, verbose_name='Понедельник')
    mondayTime = models.TimeField(null=True, blank=True, verbose_name='Время занятий в понедельник')
    mondayTimeFinal = models.TimeField(null=True, blank=True, verbose_name='Время окончания занятий в понедельник')
    tuesday = models.BooleanField(default=False, verbose_name='Вторник')
    tuesdayTime = models.TimeField(null=True, blank=True, verbose_name='Время занятий во вторник')
    tuesdayTimeFinal = models.TimeField(null=True, blank=True, verbose_name='Время окончания занятий во вторник')
    wednesday = models.BooleanField(default=False, verbose_name='Среда')
    wednesdayTime = models.TimeField(null=True, blank=True, verbose_name='Время занятий в Среду')
    wednesdayTimeFinal = models.TimeField(null=True, blank=True, verbose_name='Время окончания занятий в среду')
    thursday = models.BooleanField(default=False, verbose_name='Четверг')
    thursdayTime = models.TimeField(null=True, blank=True, verbose_name='Время занятий в четверг')
    thursdayTimeFinal = models.TimeField(null=True, blank=True, verbose_name='Время окончания занятий в четверг')
    friday = models.BooleanField(default=False, verbose_name='Пятница')
    fridayTime = models.TimeField(null=True, blank=True, verbose_name='Время занятий в пятницу')
    fridayTimeFinal = models.TimeField(null=True, blank=True, verbose_name='Время окончания занятий в пятницу')
    saturday = models.BooleanField(default=False, verbose_name='Суббота')
    saturdayTime = models.TimeField(null=True, blank=True, verbose_name='Время занятий в субботу')
    saturdayTimeFinal = models.TimeField(null=True, blank=True, verbose_name='Время окончания занятий в субботу')
    sunday = models.BooleanField(default=False, verbose_name='Воскресенье')
    sundayTime = models.TimeField(null=True, blank=True, verbose_name='Время занятий в воскресенье')
    sundayTimeFinal = models.TimeField(null=True, blank=True, verbose_name='Время окончания занятий в воскресенье')
    comment = models.TextField( null=True, blank=True, verbose_name='Комментарий', default="")

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'

    def __str__(self):
        return f"Расписание для группы {self.group}"


class LessonFeedback(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', related_name='feedbacks')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='lesson_feedbacks')
    feedback = models.TextField('Отзыв', default='Дз еще не проверялось')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    mark_field = models.IntegerField('Оценка за урок', default=0)
    file_field = models.FileField('Дз ученика')
    HomeWorkCheck = models.BooleanField(default=False, verbose_name='Проверка ДЗ')



    class Meta:
        verbose_name = 'Проверка ДЗ'
        verbose_name_plural = 'Проверка ДЗ'

    def __str__(self):
        return f"Feedback on {self.lesson.name} by {self.user.username}"


