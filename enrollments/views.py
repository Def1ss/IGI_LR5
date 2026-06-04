from django.shortcuts import render, redirect, get_object_or_404
from .models import IndividualSession, GroupEnrollment
from workouts.models import Group, WorkoutType
from users.models import Instructor, Client
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import calendar
import datetime

@login_required
def session_list(request):
    sessions = IndividualSession.objects.all()
    workout_types = WorkoutType.objects.filter(category='individual')
    instructors = Instructor.objects.all()

    client = getattr(request.user, 'client', None)
    instructor = getattr(request.user, 'instructor', None)

    if request.user.is_superuser:
        sessions = IndividualSession.objects.none()

    elif instructor:
        sessions = sessions.filter(instructor=instructor)

    elif client:
        sessions = sessions.filter(client=client)

    today = datetime.date.today()

    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    MONTH_NAMES_RU = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь',
    }

    month_name = MONTH_NAMES_RU[month]

    cal = calendar.TextCalendar(firstweekday=0)

    text_calendar = cal.formatmonth(
        year,
        month
    )

    return render(request, 'enrollments/session_list.html', {
        'sessions': sessions,
        'workout_types': workout_types,
        'instructors': instructors,

        'year': year,
        'month': month,

        'prev_year': prev_year,
        'prev_month': prev_month,

        'next_year': next_year,
        'next_month': next_month,

        'month_name': month_name,
        'text_calendar': text_calendar,
    })

@login_required
def enroll_group(request, group_id):
    client = getattr(request.user, 'client', None)
    if not client:
        messages.error(request, 'Только зарегистрированные клиенты могут записываться!')
        return redirect('workouts:schedule')
    
    # Check card
    from users.models import ClubCard
    if not ClubCard.objects.filter(client=client).exists():
        messages.error(request, 'Ошибка! Для записи требуется активная клубная карта!')
        return redirect('users:profile')
        
    group = get_object_or_404(Group, id=group_id)
    GroupEnrollment.objects.create(
        client=client,
        group=group,
        paid_amount=group.workout_type.price_per_cycle,
        payment_status='paid'
    )
    messages.success(request, f"Вы успешно записались на направление: {group.name}!")
    return redirect('workouts:schedule')

@login_required
def schedule_session(request):

    if request.user.is_superuser or hasattr(request.user, 'instructor'):
        messages.error(
            request,
            'Только клиенты могут бронировать индивидуальные тренировки.'
        )
        return redirect('enrollments:session_list')
    if request.method == "POST":
        client = getattr(request.user, 'client', None)
        if not client:
            return redirect('content:home')
            
        instructor_id = request.POST.get('instructor_id')
        workout_type_id = request.POST.get('workout_type_id')
        session_date = request.POST.get('session_date')
        
        IndividualSession.objects.create(
            client=client,
            instructor_id=instructor_id,
            workout_type_id=workout_type_id,
            session_date=session_date,
            status='scheduled'
        )
        messages.success(request, 'Индивидуальная тренировка зарезервирована!')
    return redirect('enrollments:session_list')
