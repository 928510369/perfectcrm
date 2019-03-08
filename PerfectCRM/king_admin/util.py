from django.db.models import Q
from django.utils.timezone import datetime,timedelta
def filter_objs(request,modeladmin):
    filter_dict={}

    request_other_fileds=["o","page","q_field"]
    today_ele=datetime.now().date()
   #  date_list=[  ['今天', datetime.now().date()],
   # ["昨天", today_ele - timedelta(days=1)],
   # ["近7天", today_ele - timedelta(days=7)],
   # ["本月", today_ele.replace(day=1)],
   # ["近30天", today_ele - timedelta(days=30)],
   # ["近90天", today_ele - timedelta(days=90)],
   # ["近180天", today_ele - timedelta(days=180)],
   # ["本年", today_ele.replace(month=1, day=1)],
   # ["近一年", today_ele - timedelta(days=365)]]


    for k,v in request.GET.items():

        if k in request_other_fileds:
            continue
        if v :
            filter_dict[k]=v



    date_time=filter_dict.get("date__gte","")

    return modeladmin.model.objects.filter(**filter_dict).\
        order_by("-%s" %modeladmin.ordering if modeladmin.ordering else "-id")\
    ,filter_dict

def sort_table(request,objs):
    order_key=request.GET.get("o","")

    if order_key:
        if order_key.startswith("-"):
            order_key=order_key.strip("-")
        else:
            order_key="-%s"%(order_key)

        objs = objs.order_by(order_key)
    else:
        order_key=""


    return objs,order_key
def table_search(request,obj,modeladmin):
    q_field=request.GET.get("q_field","")
    q=Q()
    q.connector="OR"

    for filed in modeladmin.search_fields:#这里会出现bug,不可以外键字段进行模糊匹配

        q.children.append(("%s__contains"%(filed),q_field))
    #print("q",q)
    objs=obj.filter(q)

    return objs,q_field