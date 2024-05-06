from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from urllib.parse import quote
from .models import CustomUser, Lesson, LessonFeedback, Themes, Schedule
import os
from django.contrib.auth.admin import UserAdmin
from django.conf import settings


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'first_name', 'last_name', 'date_of_next_payment', 'course_bought', 'score', 'birth_date', 'email')
    # TODO: При выпуске в прод раскоментить , 'ip', 'city', 'org'
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        ('Информация о пользователе', {'fields': (
            'username', 'password', 'first_name', 'last_name', 'email', 'date_of_next_payment', 'course_bought',
            'score',
            'birth_date')}),
        ('Группы', {'fields': ('groups',)}),
        # TODO: При выпуске в прод раскоментить
        #('Информация по входам пользователя', {'fields': ('ip', 'city', 'org')})
    )


class LessonFeedbackAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'HomeWorkCheck', 'created_at', 'mark_field', 'download_homework')
    search_fields = ('user__username', 'lesson__name', 'HomeWorkCheck')
    list_filter = ('user', 'lesson', 'HomeWorkCheck', 'lesson__theme')
    readonly_fields = ('file_field',)

    def download_homework(self, obj):
        if obj.file_field:
            url = obj.file_field.url
            custom_filename = f"{quote(obj.user.username)}_{quote(obj.lesson.name)}"
            return format_html(f'<a href="{url}" download="{custom_filename}">Скачать</a>')
        else:
            return "Нет файла"

    download_homework.short_description = "Домашнее задание"

    def download_file(self, request, queryset):
        selected = queryset.first()
        if selected and selected.file_field:
            file_path = selected.file_field.path
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    filename = f"{quote(selected.user.username)}_{quote(selected.lesson.name)}"
                    response = HttpResponse(fh.read(), content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
                    return response
        self.message_user(request, "File not found or no file selected.", level='error')
        return None

    download_file.short_description = "Download Selected Homework"


class LessonInline(admin.TabularInline):  # Используем TabularInline для компактности
    model = Lesson
    extra = 1


class ThemesAdmin(admin.ModelAdmin):
    inlines = [LessonInline]


admin.site.register(Schedule)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Lesson)
admin.site.register(LessonFeedback, LessonFeedbackAdmin)
admin.site.register(Themes, ThemesAdmin)
