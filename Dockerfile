# Используем базовый образ Python
FROM python:3.11

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Копируем файлы проекта внутрь контейнера
COPY . /app/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Задаем переменную STATIC_ROOT
ENV STATIC_ROOT=/app/staticfiles
ENV MEDIA_ROOT=/app/media

# Выполняем миграции
RUN python manage.py migrate

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Открываем порт 8080
EXPOSE 8080

# Команда для запуска сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]