from django.shortcuts import render,redirect
from king_admin import king_admin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.util import filter_objs,sort_table,table_search
from king_admin.forms import create_model_form
from django.contrib.auth.decorators import login_required
from crm.permission.permission import check_permission
from collections import Iterable
import importlib
# Create your views here.


@login_required
def index(request):

    return render(request, "king_admin/table_index.html", {"admindict":king_admin.AdminDict})

@check_permission
@login_required
def display_table_objs(request,app_name,table_name):
    # m=importlib.import_module("%s"%(app_name))

    modeladmin=king_admin.AdminDict[app_name][table_name]
    # contact_list = modeladmin.model.objects.order_by('id')
    # print(type(contact_list), contact_list)
    if request.method=="POST":

        obj_ids=request.POST.get("obj_ids")
        # obj_idss=obj_ids.split(',')
        # print(obj_idss)
        action=request.POST.get("action_name")
        if obj_ids:
            obj_list=modeladmin.model.objects.filter(id__in=obj_ids.split(','))
        else:
            raise KeyError
        print("action",action)
        if hasattr(modeladmin,action):
            action_way=getattr(modeladmin,action)

            request._admin_action=action
            return action_way(modeladmin,request,obj_list)

    contact_list,filter_dict=filter_objs(request,modeladmin)

    contact_list,search_filed=table_search(request,contact_list,modeladmin)

    contact_list,order_key=sort_table(request,contact_list)
    paginator = Paginator(contact_list, modeladmin.list_per_page)  # Show 25 contacts per page
    previous_key=request.GET.get("o","")
    # date_time2=request.GET.get("date__gte","")
    # print(date_time2)
    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)

    return render(request, "king_admin/table_objs.html", {"modeladmin":modeladmin, "query_sets":query_sets,\
                                                         "filter_dict":filter_dict,
                                                         "order_key":order_key,
                                                         "previous_key":previous_key,
                                                         "search_filed":search_filed,
                                                         "app_name": app_name, "table_name": table_name
                                                          })

@login_required
def table_objs_add(request,app_name,table_name):
    modeladmin = king_admin.AdminDict[app_name][table_name]

    model_form_class = create_model_form(request, modeladmin)
    modeladmin.is_add_form=True
    if request.method=="POST":
        # print(request.POST)
        model_form_obj=model_form_class(request.POST)
        if model_form_obj.is_valid():
            model_form_obj.save()
            return redirect(request.path.replace("/add/","/"))
    else:

        model_form_obj = model_form_class()
        # model_form_obj.instance.id = 0#low
    # for i in model_form_obj:
    #     print(type(i),"ul",i)
    # print(type(model_form_obj))
    return render(request, "king_admin/table_obj_add.html", {"modelform":model_form_obj, "modeladmin":modeladmin, })
@check_permission
@login_required
def table_objs_change(request,app_name,table_name,obj_id):
    modeladmin = king_admin.AdminDict[app_name][table_name]

    model_form_class=create_model_form(request,modeladmin)
    obj=modeladmin.model.objects.get(id=obj_id)

    model_form_obj=model_form_class(instance=obj)

    if request.method=="POST":
        model_form_obj=model_form_class(request.POST,instance=obj)
        if model_form_obj.is_valid():
            model_form_obj.save()
            return redirect("/king_admin/%s/%s/"%(app_name,table_name))
    else:
        model_form_obj = model_form_class(instance=obj)


    return render(request, "king_admin/table_obj_change.html", {"modelform":model_form_obj, "modeladmin":modeladmin,\
                                                              "app_name":app_name,"table_name":table_name})
@login_required
def table_objs_delete(request,app_name,table_name,obj_id):

    modeladmin = king_admin.AdminDict[app_name][table_name]
    obj = modeladmin.model.objects.get(id=obj_id)
    if modeladmin.tablereadonly_option:
        errors={"tablereadonly":"the table can't delete,"}
    else:
        errors={}
    if request.method=="POST":
        if not modeladmin.tablereadonly_option:
            obj.delete()
        return redirect("/king_admin/%s/%s/"%(app_name,table_name))

    return render(request, "king_admin/table_obj_delete.html", {"objs":obj, "app_name":app_name, "table_name":table_name, "errors":errors})

@login_required
def password_reset(request,app_name,table_name,obj_id):
    modeladmin = king_admin.AdminDict[app_name][table_name]


    obj = modeladmin.model.objects.get(id=obj_id)
    errors = {}
    if request.method=="POST":

        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1==password2:
            if  len(password1)>5:
                obj.set_password(password2)
                obj.save()
                return redirect(request.path.rstrip("password/"))
            else:
                errors["password short"]="password is less than 6 chars"
        else:
            errors["passwors error"]="two password is not one"


    return render(request, "king_admin/password_reset.html", {"obj":obj, "errors":errors})