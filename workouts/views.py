from django.shortcuts import render, redirect, get_object_or_404
import calendar
import datetime
from .models import ScheduledClass, WorkoutType, Group, GymHall
from django.contrib.auth.decorators import login_required
from django.contrib import messages

MONTH_NAMES_RU = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
    7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

def schedule_view(request):
    try:
        year = int(request.GET.get('year', 2026))
        month = int(request.GET.get('month', 6))
    except ValueError:
        year = 2026
        month = 6

    if month < 1 or month > 12:
        month = 6
    if year < 2000 or year > 2100:
        year = 2026

    # Prev and Next month calculate
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

    month_name = MONTH_NAMES_RU.get(month, 'Июнь')

    # text calendar
    cal = calendar.TextCalendar(firstweekday=0)
    text_calendar = cal.formatmonth(year, month)

    filters = {
        'date': request.GET.get('date', ''),
        'group': request.GET.get('group', ''),
        'hall': request.GET.get('hall', ''),
        'q': request.GET.get('q', ''),
    }

    classes_list = ScheduledClass.objects.all().order_by('start_time')

    if filters['date']:
        classes_list = classes_list.filter(start_time__date=filters['date'])
    if filters['group']:
        classes_list = classes_list.filter(group_id=filters['group'])
    if filters['hall']:
        classes_list = classes_list.filter(hall_id=filters['hall'])
    if filters['q']:
        q = filters['q']
        classes_list = classes_list.filter(group__name__icontains=q) | classes_list.filter(group__workout_type__name__icontains=q)

    from django.core.paginator import Paginator
    paginator = Paginator(classes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    client = None
    enrolled_group_ids = []
    if request.user.is_authenticated:
        client = getattr(request.user, 'client', None)
        if client:
            from enrollments.models import GroupEnrollment
            enrolled_group_ids = list(GroupEnrollment.objects.filter(client=client).values_list('group_id', flat=True))

    groups = Group.objects.all()
    halls = [(h.id, h.name) for h in GymHall.objects.all()]
    workout_types = WorkoutType.objects.all()

    return render(request, 'workouts/schedule.html', {
        'classes': page_obj,
        'workout_types': workout_types,
        'groups': groups,
        'halls': halls,
        'filters': filters,
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'month_name': month_name,
        'text_calendar': text_calendar,
        'client': client,
        'enrolled_group_ids': enrolled_group_ids,
    })

@login_required
def bulk_price(request):
    if request.user.is_superuser:
        if request.method == "POST":
            wtype_id = request.POST.get('workout_type_id')
            percent = float(request.POST.get('percent', 10))
            if wtype_id:
                try:
                    wt = WorkoutType.objects.get(id=wtype_id)
                    factor = 1 + percent / 100
                    from decimal import Decimal
                    wt.price_per_cycle = wt.price_per_cycle * Decimal(str(factor))
                    wt.price_per_session = wt.price_per_session * Decimal(str(factor))
                    wt.save()
                    messages.success(request, f"Цены услуги {wt.name} повышены на {percent}%")
                except WorkoutType.DoesNotExist:
                    pass
    return redirect('workouts:schedule')

@login_required
def enroll_group(request, group_id):
    client = getattr(request.user, 'client', None)
    if request.user.is_superuser:
        messages.error(
            request,
            'Администраторы не могут записываться на групповые занятия.'
        )
        return redirect('workouts:schedule')
    if not client:
        messages.error(request, 'Только клиенты могут записываться!')
        return redirect('workouts:schedule')

    from users.models import ClubCard
    if not ClubCard.objects.filter(client=client).exists():
        messages.error(request, 'Ошибка! Для записи требуется активная клубная карта!')
        return redirect('users:profile')

    group = get_object_or_404(Group, id=group_id)
    promo_code = request.POST.get('promo_code', '').strip()
    price = group.workout_type.price_per_cycle
    discount_msg = ""

    if promo_code:
        from promocodes.models import PromoCode
        try:
            matched = PromoCode.objects.get(code__iexact=promo_code)
            if matched.is_active:
                from decimal import Decimal
                discount = (price * Decimal(str(matched.discount_percent))) / Decimal('100')
                price = price - discount
                discount_msg = f" Применен промокод {matched.code} со скидкой {matched.discount_percent}%!"
        except PromoCode.DoesNotExist:
            pass

    from enrollments.models import GroupEnrollment
    GroupEnrollment.objects.create(
        client=client,
        group=group,
        paid_amount=price,
        payment_status='paid'
    )
    messages.success(request, f"Вы успешно записались на направление: {group.name}!{discount_msg}")
    return redirect('workouts:schedule')
