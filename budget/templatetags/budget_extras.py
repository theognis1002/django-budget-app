from datetime import datetime, timedelta

from django import template

register = template.Library()


@register.filter(name="days_until")
def days_until(value):
    """Counts days until project due date"""
    return (datetime.now().date() - value).days * -1
