import datetime
from django.utils import timezone

def global_context(request):
    currency = request.session.get('selected_currency', 'BYN')
    # Mock conversion
    rate = 1.0
    if currency == 'USD':
        rate = 0.31
    elif currency == 'EUR':
        rate = 0.28
    
    return {
        'server_now': datetime.datetime.now(),
        'server_timezone': timezone.get_current_timezone_name(),
        'selected_currency': currency,
        'example_conversion': f"100 BYN ≈ {round(100*0.31, 2)} USD / {round(100*0.28, 2)} EUR",
    }
