from django.shortcuts import render
from .models import PromoCode

def promo_list(request):
    promos = PromoCode.objects.all()
    # Check form verification
    checking_code = request.GET.get('check_code')
    result = None
    if checking_code:
        try:
            matched = PromoCode.objects.get(code__iexact=checking_code)
            if matched.is_active:
                result = f"✅ Активен! Скидка: {matched.discount_percent}% на {matched.applicable_to}"
            else:
                result = "❌ Действие промокода прекращено!"
        except PromoCode.DoesNotExist:
            result = "❌ Промокода не существует!"
            
    return render(request, 'promocodes/list.html', {'promos': promos, 'result': result, 'check_code': checking_code})
