from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from collections import Iterable
from django.core.exceptions import FieldDoesNotExist



register=template.Library()

@register.simple_tag
def render_enroll_extract(enroll_obj):
    return enroll_obj.enrolled_class.contract.template
