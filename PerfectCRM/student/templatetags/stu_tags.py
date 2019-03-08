from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from collections import Iterable
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Sum
register=template.Library()

@register.simple_tag
def get_score(enroll_obj,customer_obj):
    study_record_list=enroll_obj.studyrecord_set.filter(course_record__from_class_id=enroll_obj.enrolled_class.id)

    score_sum=study_record_list.aggregate(Sum("score"))

    return  score_sum