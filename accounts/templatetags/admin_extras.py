# In accounts/templatetags/admin_extras.py

from django import template
from django.contrib.auth.models import User
from django.db.models import Sum

register = template.Library()

@register.simple_tag
def get_top_purchaser():
    """
    Finds the user who has purchased the most movies.
    """
    top_user = User.objects.annotate(
        total_movies_purchased=Sum('order__item__quantity')
    ).order_by('-total_movies_purchased').first()
    
    return top_user