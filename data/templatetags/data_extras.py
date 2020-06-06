from django import template

register = template.Library()


@register.filter
def as_percentage_of(part, whole):
    part = part or 0
    whole = whole or 0

    try:
        percentage = round(float(part) / whole * 100, 1)
        if percentage % 1 == 0:
            percentage = int(percentage)
        return f"{percentage}%"
    except (ValueError, ZeroDivisionError):
        return "0%"
