from django import template

register = template.Library()

@register.filter(name='usd_to_inr')
def usd_to_inr(value):
    """Convert a USD amount to INR at a fixed rate 1 USD = 83 INR.
    Rounds to whole number and formats with commas, returns a string prefixed with ₹.
    If value is not numeric, returns it unchanged.
    """
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return value

    inr = round(amount * 83)
    # Format with commas for readability
    return f"₹{inr:,}"
