from  crm import models
from django.shortcuts import render,redirect,HttpResponse
from django.forms import ValidationError
from django.utils.translation import ugettext as _
class BaseAdmin():
    list_display=[]
    list_filters=[]
    list_per_page = 10
    search_fields=[]
    ordering=None
    filter_horizontal=None
    actions = ("printobj", "delete_selected_option")
    readonly_fields=()
    tablereadonly_option=False
    modelform_exclude_fields=()
    def printobj(self,request,objs):
        print(self,request,objs)
        return redirect(request.path)
    def default_form_validation(self):
        '''用户可以在此进行自定义的表单验证，相当于django form的clean方法'''
        pass

    def delete_selected_option(self,request,objs):

        app_name=self.model._meta.app_label
        table_name=self.model._meta.model_name
        delete_sure=request.POST.get("delete_sure")
        if self.tablereadonly_option:
            errors = {"tablereadonly": "the table can't delete,"}
        else:
            errors = {}
        if delete_sure=="yes":
            if  not self.tablereadonly_option:
                objs.delete()
            return redirect("/king_admin/%s/%s/" % (app_name, table_name))
        id_list=','.join([str(i.id) for i in objs])

        return render(request,"king_admin/table_obj_delete.html",{"objs":objs,
                                                              "admin_class":self,
                                                              "app_name": app_name,
                                                              "table_name":table_name,
                                                                "id_list":id_list,
                                                               "action":request._admin_action,
                                                             "errors":errors
                                                                    })

class CourseRecordAdmin(BaseAdmin):
    list_display = ("from_class","day_num","teacher","has_homework","homework_title","homework_content","outline")
    search_fields = [ 'day_num']

    actions = ("initialize_studyrecord",)

    def initialize_studyrecord(self,request,queryset):
        print(self,request,queryset)
        if len(queryset)>1:
            return HttpResponse("你只允许同时对一个课程进行操作")


        print(queryset[0].from_class.enrollment_set.all())

        enroll_obj_list=[]
        for enroll_obj in queryset[0].from_class.enrollment_set.all():
            enroll_obj_list.append(models.StudyRecord(
                student=enroll_obj,
                course_record=queryset[0],
                attendance=0,
                score=0,

            ))
        try:
            models.StudyRecord.objects.bulk_create(enroll_obj_list)
            return redirect("/king_admin/crm/studyrecord/?course_record=%s"%(queryset[0].day_num))
        except Exception as e:
            return HttpResponse("学习记录已存在，不可重复创建")




    initialize_studyrecord.display_name = "初始化本课程的学习记录"


class StudyRecordAdmin(BaseAdmin):
    list_display =("student","course_record","attendance","score")
    list_filters = ("course_record",)
class CustomerAdmin(BaseAdmin):
    list_display=['id',"qq","name","phone","source","date","status","consult_course","consultant","enroll"]
    list_filters = ["source","status","consultant","date"]
    list_per_page = 3
    search_fields = ["qq","name","consultant__name"]
    ordering = None
    filter_horizontal =("tags",)
    actions = ("printobj", "delete_selected_option","test")
    readonly_fields=("qq","consultant",'tags')
    #tablereadonly_option = True
    def test(self,request,objs):
        return redirect(request.path)
    test.display_name = "测试动作"
    def default_form_validation(self):
        print("自定制valitation")
        coltant_content=self.cleaned_data.get("content")

        if len(coltant_content)<10:
            return self.ValidationError(("%(field)s 咨询内容记录不能少于10个字符"), code="invalid",
                            params={"field": "content", })


    def clean_name(self):
        #("name clean validation:", self.cleaned_data["name"])

        if not self.cleaned_data["name"]:
            self.add_error('name', "cannot be null")

    def enroll(self):
        if self.instance.status==0:
            link_path="报名新课程"
        else:
            link_path="进入报名"
        return """<a href="/crm/customer/%s/enrollment/">%s</a>"""%(self.instance.id,link_path)

    enroll.display_name="报名"
class UserProfileAdmin(BaseAdmin):
    list_display = ["id","email","name"]
    filter_horizontal = ("roles",)
    readonly_fields = ("password",)
    list_per_page = 2
    filter_horizontal = ("groups","user_permissions")
    modelform_exclude_fields=("last_login",)
class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['id', "customer","content","consultant","intention","date"]
    list_filters = ["intention", ]
    list_per_page = 3
    search_fields = ["id"]
    filter_horizontal = ("tags",)


AdminDict={}
def register(model_class,admin_class=None):
    if model_class._meta.app_label not in AdminDict:
        AdminDict[model_class._meta.app_label]={}
    admin_class.model=model_class
    AdminDict[model_class._meta.app_label][model_class._meta.model_name]=admin_class

register(models.Customer,CustomerAdmin)
register(models.UserProfile,UserProfileAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
register(models.CourseRecord,CourseRecordAdmin)
register(models.StudyRecord,StudyRecordAdmin)