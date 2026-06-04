from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def convert_price(context, value):
    request = context.get('request')
    currency = 'BYN'
    if request:
        currency = request.session.get('selected_currency', 'BYN')
    
    try:
        val = float(value)
    except (ValueError, TypeError):
        return f"{value} BYN"
    
    if currency == 'USD':
        return "$" + f"{val / 3.25:.2f}"
    elif currency == 'EUR':
        return f"€{val / 3.51:.2f}"
    else:
        return f"{val:.2f} BYN"
