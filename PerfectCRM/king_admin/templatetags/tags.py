from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from collections import Iterable
from django.core.exceptions import FieldDoesNotExist
register=template.Library()

@register.simple_tag()
def render_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):

    return admin_class.model.objects.all()


@register.simple_tag()
def render_querys(request,obj,admin_class):
    row_ele=""

    for index,column in enumerate(admin_class.list_display):
        try:
            field_obj = obj._meta.get_field(column)

            if field_obj.choices:
                # print(field_obj)

                column_data= getattr(obj,"get_%s_display" % column)()
            else:

                column_data=getattr(obj,column)

            if type(column_data).__name__ == 'datetime':
                column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
            if index==0:
                column_first_data=getattr(obj,column)
                column_data="""<a href="%s%s/change">%s</a>"""%(request.path,obj.id,column_first_data)
        except FieldDoesNotExist as e:
            admin_func =getattr(admin_class,column)
            admin_class.instance=obj
            column_data=admin_func()
        row_ele += "<td>%s</td>" % column_data
    return mark_safe(row_ele)

@register.simple_tag()
def render_page_ele(loop,query_sets,filter_dict):
    filters = ""
    for k, v in filter_dict.items():
        filters += "&%s=%s" % (k, v)
    if abs(loop-query_sets.number)<=2:
        page_class=""
        if loop==query_sets.number:
            page_class="active"
        page_ele=""" <li class=%s><a href="?page=%s%s">%s</a></li>"""%(page_class,loop,filters,loop)
        return mark_safe(page_ele)
    else:
        return ""


@register.simple_tag()
def render_pages(query_sets,filter_dict,previous_key,search_filed):
    filters = ""
    pages_ele = ""
    page_class = ""
    add_dotted=False
    if not previous_key:
        previous_key=""


    for k, v in filter_dict.items():

        filters += "&%s=%s" % (k, v)
    for page_num in query_sets.paginator.page_range:
        # print(query_sets.paginator.num_pages,page_num)
        if page_num<3 or query_sets.paginator.num_pages-page_num<2 \
               or abs(page_num-query_sets.number)<=1:
            page_class = ""
            if page_num == query_sets.number:
                add_dotted = False
                page_class = "active"
            pages_ele += """ <li class=%s><a href="?page=%s%s&o=%s&q_field=%s">%s</a></li>""" % (
            page_class, page_num, filters,previous_key,search_filed,page_num)
        # elif abs(page_num-query_sets.number)<=1:
        #     page_class=""
        #     if page_num==query_sets.number:
        #         add_dotted = False
        #         page_class="active"
        #     pages_ele+=""" <li class=%s><a href="?page=%s%s">%s</a></li>"""%(page_class,page_num,filters,page_num)

        else:
            if add_dotted==False:
                pages_ele+=""" <li class=%s><a href="javascript:void(0)">...</a></li>"""%(page_class)
                add_dotted=True
    return mark_safe(pages_ele)



@register.simple_tag()
def render_select (modeladmin,render_filter,filter_dict,date_select):

    select_ele="""<select name={filter_date} class="form-control"><option value="">------</option>"""
    selected=""
    field_obj=modeladmin.model._meta.get_field(render_filter)

    if field_obj.choices:
        for choice_item in field_obj.choices:

            if filter_dict.get(render_filter)==str(choice_item[0]):
                selected="selected"

            select_ele+="<option  value=%s %s >%s</option>"%(choice_item[0],selected,choice_item[1])
            selected=""

    if type(field_obj).__name__=='ForeignKey':

        for choice_item in field_obj.get_choices()[1:]:

            if filter_dict.get(render_filter) == str(choice_item[0]):
                selected = "selected"

            select_ele += "<option value=%s %s >%s</option>" % (choice_item[0],selected, choice_item[1])
            selected = ""

    if type(field_obj).__name__ in ["DateField","DateTimeField"]:
        date_select=filter_dict.get("date__gte","")
        date_els = []
        today_ele = datetime.now().date()
        date_els.append(['今天', datetime.now().date()])
        date_els.append(["昨天", today_ele - timedelta(days=1)])
        date_els.append(["近7天", today_ele - timedelta(days=7)])
        date_els.append(["本月", today_ele.replace(day=1)])
        date_els.append(["近30天", today_ele - timedelta(days=30)])
        date_els.append(["近90天", today_ele - timedelta(days=90)])
        date_els.append(["近180天", today_ele - timedelta(days=180)])
        date_els.append(["本年", today_ele.replace(month=1, day=1)])
        date_els.append(["近一年", today_ele - timedelta(days=365)])


        for item in date_els:

            if str(item[1])==date_select:
                selected="selected"

            select_ele +="<option value=%s %s >%s</option>" % (item[1], selected, item[0])
            selected=""
        filter_name_value="%s__gte"%render_filter
    else:
        filter_name_value =render_filter
    select_ele+="</select>"

    select_ele=select_ele.format(filter_date=filter_name_value)

    return mark_safe(select_ele)

@register.simple_tag()
def page_filters (filter_dict):
    filters=""
    for k,v in filter_dict.items():
        filters+="&%s=%s"%(k,v)

    return mark_safe(filters)


@register.simple_tag()
def build_header_column(column,order_key,filter_dict,previous_key,search_filed,admin_class):


    filters = ""
    sort_logo=""
    for k, v in filter_dict.items():
        filters += "&%s=%s" % (k, v)

    if column==order_key.strip("-"):
        o_href=order_key
        if previous_key.startswith("-"):
            sort_logo="glyphicon glyphicon-chevron-down"
        else:
            sort_logo="glyphicon glyphicon-chevron-up"


    else:
        o_href=column




    try:
        column_verbose_name = admin_class.model._meta.get_field(column).verbose_name.upper()
    except FieldDoesNotExist  as e:
        column_verbose_name = getattr(admin_class,column).display_name.upper()
        th_ele = '''<th><a href="javascript:void(0);">{column}</a></th>'''.format(column=column_verbose_name)
        return mark_safe(th_ele)
    th_ele = """<th><a href="?o={orderkey}&{filter_list}&q_field={q_filed}">{col}</a><span class="{sort_logos}"></span></th>""".format( \
        orderkey=o_href, col=column_verbose_name, filter_list=filters, sort_logos=sort_logo, q_filed=search_filed)
    return mark_safe(th_ele)

@register.simple_tag()
def sort_a (previous_key):
    if not previous_key:
        previous_key = ""
    return "o=%s"%previous_key


@register.simple_tag()
def get_m2m_onj_list( modeladmin,modelform,field):
    # print(field)
    all_objs=getattr(modeladmin.model,field.name).rel.to.objects.all()
    if modelform.instance.id:
        selectd_objs=getattr(modelform.instance,field.name).all()
        # print(all_objs,selectd_objs)
        stand_list = []
        for obj in all_objs:
            if obj not in selectd_objs:
                stand_list.append(obj)
        # print(obj.rel.to.objects.all())
        return stand_list
    else:
        return all_objs

@register.simple_tag()
def get_m2m_select_objs(modelform,field):
    if modelform.instance.id:
        modelform_obj=getattr(modelform.instance,field.name)


        return modelform_obj.all()
    return
@register.simple_tag()
def print_obj_methods(obj):
    print("debug %s"%obj)
    print(dir(obj))

def revesed_eles(objs):

    ul_ele="<ul>"
    for obj in objs:
        li_ele="""<li>%s %s</li>"""%(obj._meta.verbose_name,obj.__str__())
        ul_ele +=li_ele
        for m2m_field in obj._meta.local_many_to_many:
            # print(type(m2m_field),m2m_field)
            sub_ul="<ul>"
            m2m_field_obj=getattr(obj,m2m_field.name)

            for o in m2m_field_obj.all():
                li_ele = """<li>%s %s</li>""" % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul+=li_ele
            sub_ul += "</ul>"
            ul_ele+=sub_ul
        for reletes_obj in obj._meta.related_objects:
            # print("releted_obj",reletes_obj)
            if "ManyToManyRel" in reletes_obj.__repr__():
                if hasattr(obj, reletes_obj.get_accessor_name()):  # (obj,"customerfollowup_set")

                    accessor_obj = getattr(obj, reletes_obj.get_accessor_name())

                    if hasattr(accessor_obj, "all"):
                        target_objs = accessor_obj.all()
                    else:
                        target_objs = accessor_obj
                    sub_ul = "<ul>"
                    for o in target_objs:
                        li_ele = """<li style="color:red;">%s %s</li>""" % (o._meta.verbose_name, o.__str__().strip("<>"))
                        sub_ul += li_ele
                    sub_ul += "</ul>"
                    ul_ele += sub_ul

            elif hasattr(obj,reletes_obj.get_accessor_name()):#(obj,"customerfollowup_set")
                # print("reletes_obj.get_accessor_name",type(obj),obj,type(reletes_obj.get_accessor_name()),reletes_obj.get_accessor_name())
                accessor_obj=getattr(obj,reletes_obj.get_accessor_name())

                if hasattr(accessor_obj,"all"):
                    target_objs=accessor_obj.all()
                else:
                    target_objs=accessor_obj



                if len(target_objs) > 0:
                    node=revesed_eles(target_objs)
                    # print("node",node)
                    ul_ele+=node

        ul_ele+="</ul>"
    return ul_ele

@register.simple_tag()
def display_delete_obj(objs):

    # objs=[obj,]
    if objs:
        if not isinstance(objs,Iterable):
            objs = [objs, ]
        # obj_model=objs._meta.model
        # print(objs)
        # return mark_safe(recursive_related_objs_lookup(objs))
        return mark_safe(revesed_eles(objs))
@register.simple_tag()
def display_action_name(modeladmin,action):
    action_way=getattr(modeladmin,action)
    # print(type(action),action)
    return action_way.display_name if hasattr(action_way,'display_name') else action
