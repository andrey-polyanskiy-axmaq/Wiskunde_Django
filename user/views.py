from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, ProfileEditForm
from django.http import HttpResponse
from django.conf import settings
import os
from django.utils import timezone
from .models import Lesson
from .forms import ThemeFilterForm
from .models import LessonFeedback
import logging
from datetime import timedelta, date
from .models import Schedule

from django.utils.timezone import localtime

logging.basicConfig(level=logging.DEBUG,
                    filename='debug.log',
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('auth_backend')


def user_check(request):
    auth_status = request.user.is_authenticated
    return auth_status


def user_paied(request):
    return not (request.user.date_of_next_payment < date.today()) or request.user.course_bought


def logout_user(request):
    logger.debug(f"Logging out user: {request.user.username}")
    logout(request)
    return redirect('home')


def index(request):
    if user_check(request):
        logger.debug(f"Index page accessed by user: {request.user.username}")
        context = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'date_joined': request.user.date_joined,
            'last_login': request.user.last_login,
        }
        return render(request, 'user/index.html', context)

    else:
        logger.debug("Index page accessed by anonymous user")
        return render(request, 'user/error.html', {'error': 'Вы не авторизованы. Войдите в систему'})


def profile_edit(request):
    logger.debug(f"Profile edit page accessed by user: {request.user.username}")
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProfileEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('userinfo')
            else:
                return render(request, 'user/error.html', {'error': 'Ошибка при изменение профиля'})
        else:
            form = ProfileEditForm(instance=request.user)
        return render(request, 'user/profile_edit.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            logger.debug(f"Admin has been authenticated")
            return redirect('/admin/')
        else:
            logger.debug(f"User has been authenticated by {request.user.username}")
            return redirect('userinfo')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username_or_email = cd['username']  # Используйте 'username' как общее имя для имени пользователя или email
            user = authenticate(request, username=username_or_email, password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.user.is_superuser:
                        return redirect('/admin/')
                    else:
                        return redirect('userinfo')
                else:
                    logger.debug("User account is inactive.")
                    return render(request, 'user/login.html', {'form': form, 'error': 'Ваш аккаунт неактивен.'})
            else:
                logger.debug("Incorrect credentials provided.")
                return render(request, 'user/login.html', {'form': form, 'error': 'Неправильные учетные данные.'})
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def lessons(request):
    form = ThemeFilterForm(request.GET or None)
    if user_check(request):
        if user_paied(request):
            try:
                lessons_query = Lesson.objects.filter(group=request.user.groups.all()[0].name, date__lt=timezone.now())
            except:
                return render(request, 'user/error.html', {'error': 'Уроки пока еще не выложены'})
            if lessons_query is not None:
                if form.is_valid():
                    theme = form.cleaned_data.get('theme')
                    if theme:
                        lessons_query = lessons_query.filter(theme=theme)
                all_lessons = lessons_query.order_by('-date')

                lessons_feedback = {}
                for lesson in all_lessons:
                    feedback_data = {}
                    try:
                        feedback = LessonFeedback.objects.get(lesson=lesson, user=request.user)
                        feedback_data['feedback'] = feedback.feedback
                        feedback_data['mark'] = feedback.mark_field
                        feedback_data['file_name'] = feedback.file_field.name if feedback.file_field else None
                    except LessonFeedback.DoesNotExist:
                        feedback_data['feedback'] = None
                        feedback_data['mark'] = None
                        feedback_data['file_name'] = None
                    lessons_feedback[lesson.id] = feedback_data

                return render(request, 'user/lessons.html', {
                    'form': form,
                    'lessons': all_lessons,
                    'lessons_feedback': lessons_feedback})
            else:
                return render(request, 'user/error.html', {'error': 'Никаие уроки пока еще не выложены'})
        else:
            logger.debug("Index page accessed by anonymous user")
            return render(request, 'user/error.html', {'error': 'Подписка на курс кончилась. Пожалуйста, обратитесь к администратору чтобы продлить курс. \n' +
                                                                'Учтите, что курсы приостанавливаются автоматически. Если вы считаете, что это ошибка, пожалуйста, обратитесь к администратору'})
    return render(request, 'user/error.html', {'error': 'Вы не авторизованы. Войдите в систему'})


def download_lesson_PDF_file(request, filename):
    logger.debug(f"Downloading file: {filename} by user: {request.user.username}")
    file_path = settings.BASE_DIR / 'media' / filename
    if 'pdf' in filename:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(filename)
            return response
    elif 'docx' in filename:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename="' + os.path.basename(filename) + '"'
            return response
    elif 'zip' in filename:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="' + os.path.basename(filename) + '"'
            return response
    else:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="' + os.path.basename(filename) + '"'
            return response


def upload_feedback(request):
    if user_check(request):
        if request.method == 'POST':
            # Получаем данные из формы
            lesson_id = request.POST.get('lesson_id')
            uploaded_file = request.FILES.get('file')
            logger.debug(f"Uploading feedback for lesson: {lesson_id} by user: {request.user.username}")

            # Находим соответствующий урок и текущего пользователя
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                user = request.user
            except Lesson.DoesNotExist:
                return HttpResponse('Урок не найден', status=404)

            # Проверяем, существует ли уже обратная связь для этого урока от текущего пользователя
            feedback, created = LessonFeedback.objects.get_or_create(
                lesson=lesson,
                user=user,
                defaults={'file_field': uploaded_file}  # Устанавливаем загруженный файл только если объект создается
            )

            if not created:
                feedback.file_field = uploaded_file
                feedback.save()

            return redirect('lessonsuser')
        else:
            return redirect('lessonsuser')
    else:
        return render(request, 'user/error.html', {'error': 'Ошибка при загрузке файла. Попробуйте перезагрузить '
                                                            'страницу'})


def schedule(request):
    if user_check(request):
        groups = request.user.groups.all()
        try:
            scheduleUser = Schedule.objects.filter(group=int(groups[0].name)).first()
            if scheduleUser is None:
                return render(request, 'user/error.html', {'error': 'Для вас еще не составлено расписание.'})
            today = localtime().date()
            start_week = today - timedelta(days=today.weekday())  # Monday
            week_dates = [(start_week + timedelta(days=i)) for i in range(7)]

            schedule_data = []
            for i, current_date in enumerate(week_dates):
                day_name = current_date.strftime('%A').lower()
                time = "В этот день нет занятий"  # Инициализация переменной time
                timeFinally = "В этот день нет занятий"  # Инициализация переменной timeFinally
                if day_name == 'monday' and scheduleUser.monday:
                    time = scheduleUser.mondayTime
                    timeFinally = scheduleUser.mondayTimeFinal
                elif day_name == 'tuesday' and scheduleUser and scheduleUser.tuesday:
                    time = scheduleUser.tuesdayTime
                    timeFinally = scheduleUser.tuesdayTimeFinal
                elif day_name == 'wednesday' and scheduleUser and scheduleUser.wednesday:
                    time = scheduleUser.wednesdayTime
                    timeFinally = scheduleUser.wednesdayTimeFinal
                elif day_name == 'tuesday' and scheduleUser and scheduleUser.tuesday:
                    time = scheduleUser.thursdayTime
                    timeFinally = scheduleUser.thursdayTimeFinal
                elif day_name == 'friday' and scheduleUser and scheduleUser.friday:
                    time = scheduleUser.fridayTime
                    timeFinally = scheduleUser.fridayTimeFinal
                elif day_name == 'saturday' and scheduleUser and scheduleUser.saturday:
                    time = scheduleUser.saturdayTime
                    timeFinally = scheduleUser.saturdayTimeFinal
                elif day_name == 'sunday' and scheduleUser and scheduleUser.sunday:
                    time = scheduleUser.sundayTime
                    timeFinally = scheduleUser.sundayTimeFinal
                schedule_data.append({
                    'day': current_date.strftime('%A').capitalize(),
                    'date': current_date,
                    'time': time,
                    'time_finally': timeFinally,
                    'is_today': (current_date == today)
                })

            context = {
                'class_comment': scheduleUser.comment if scheduleUser else "",
                'schedule_data': schedule_data
            }
            return render(request, 'user/schedule.html', context)
        except:
            return render(request, 'user/error.html',
                          {'error': 'Ошибка при загрузке расписания. Для вас еще не составлено расписание.'})
    else:
        return render(request, 'user/error.html', {'error': 'Вы не авторизованы'})
