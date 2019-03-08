from django.shortcuts import render,HttpResponse
from app01 import models
from django.db.models import Avg,Min,Sum,Max,F,Q
import json
from django import forms
from django.forms import fields
from django.core.validators import ValidationError
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.cache import cache_page
class LoginForm(forms.Form):
    #widget=forms.TextInput(attrs={'required':None}),
    user=forms.CharField(label="用户名",required=True,min_length=6,error_messages={"required":"用户名不能为空","min_length":"用户命不少于6个字符"})
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'type':"text"}),error_messages={"invalid":"格式不正确","required":"邮箱不能为空"})
    # password=fields.CharField(widget=forms.PasswordInput ,validators={


    # })
    userdetail=forms.ChoiceField(choices=models.Userdetiel.objects.values_list("id","info"))
    def __init__(self,*args,**kwargs):
        super(LoginForm,self).__init__(*args,**kwargs)#重写构造函数，实现ChoiceField更新
        self.fields["userdetail"].widget.choices=models.Userdetiel.objects.values_list("id","info")
    # def clean_user(self):#自定义验证
    #     if self.changed_data["user"] == "root":
    #         return self.changed_data["user"]
    #     else:
    #         raise ValidationError("你不是我想要的")

def login(request):
    print(request.method)
    if request.method=="GET":
        obj = LoginForm()
        return render(request,"login.html",{"oo":obj})
    else:
        obj = LoginForm(request.POST)
        if obj.is_valid():
            print(obj.clean())
            return HttpResponse('ok')

        return render(request,"login.html",{"oo":obj})
def login_ajax(request):
    print(request)
    if request.method=="GET":
        return render(request,"login_ajax.html")
    else:
        print(request.POST)
        obj = LoginForm(request.POST)
        if obj.is_valid():
            print(obj.clean())
            return HttpResponse('ok')
        res_error=obj.errors.as_json()#也可以用as_data,不过要序列化以及自定义序列化使用jsonCustomEncoder


        return HttpResponse(res_error)

class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
            if isinstance(field, ValidationError):
                return {'code': field.code, 'message': field.message}
            else:
                return json.JSONEncoder.default(self, field)

# Create your views here.
def date(req):
    #book=models.Book.objects.filter(id=1)[0]
    #book = models.Book.objects.filter(id__gt=2)[0]//id>2
    #book = models.Book.objects.filter(id__lt=2)[0]
    #author=models.Author.objects.filter(book__title="php").values("book__price")


    # author = models.Author.objects.filter(book__title="php").values("book__price")
    # print(author.query)


    #print(models.Book.objects.all().aggregate(Avg("price")))


    #print(models.Book.objects.all().aggregate(Max("page_num")))//聚合查询


    #print(models.Book.objects.values("color").annotate(Sum("page_num")))//分组查询
    #print(models.Book.objects.values("title").annotate(Min("page_num")).query)
    #models.Book.objects.all().update(page_num=F("page_num")+10)//对表中的一列进行操作
    #obj=models.Book.objects.filter(Q(id=2)|Q(title="python"))//用Q来构建条件
    obj = models.Book.objects.filter(Q(id=2) | ~Q(title="python"))
    print(obj)
    return  HttpResponse("ok")

def index(req):


    return render(req,"index.html")

def ajax(req):

    if req.method=="POST":
        print("req.POST",req.POST)
    return HttpResponse("ok")

def ajax_register(req):
    if req.method=="POST":
        username=req.POST.get("username")
        #print(username)
        if username=="alex":
            return HttpResponse("1")
        return HttpResponse("0")
    return render(req,"zhuce.html")


def jqurey_ajax(req):

    return render(req,"jqurey.html")
def jqurey_get(req):
    # print(req.GET)
    #print(req.POST)
    dic={'name':"alex"}
    return HttpResponse(json.dumps(dic))

def one_to_one(request):
    obj=models.User.objects.all().select_related("infi").values()
    obj2=models.User.objects.all().values()
    print(obj)
    return render(request,"test.html")
def model_test(req):
    obj=models.User(name='agou')
    obj.full_clean()
    obj.save()
    return HttpResponse("Ok")
class UserModel(ModelForm):
    class Meta:
        model=models.User
        fields="__all__"

def Modelform(request):
    if request.method=="GET":
        obj=UserModel()
        # # a=int("asd")
        # print("view")
        # print(a)
        return render(request,"modelform.html",{"obj":obj})
    else:
        print(request.POST)
        obj=UserModel(request.POST)
        if obj.is_valid():
            #obj.save()
            obj.save(commit=False)
            obj.save()
            obj.save_m2m()


        return render(request, "modelform.html",{"obj":obj})

def editmodelform(request,nid):
    if request.method=="GET":
        model_obj=models.User.objects.get(id=nid)
        obj=UserModel(instance=model_obj)
        return render(request,"mf.html",{"obj":obj,"nid":nid})
    else:
        model_obj = models.User.objects.get(id=nid)
        obj=UserModel(request.POST,instance=model_obj)
        if obj.is_valid():
            obj.save()

        return render(request, "mf.html",{"obj":obj,"nid":nid})
@cache_page(60)
def cache_test(request):
    import time
    v=time.time()
    return HttpResponse(v)

def test_signal(request):
    # user=models.Userdetiel(info="aa")
    # from first import mysignal
    # mysignal.send(sender="aaa",name="agou")
    #
    # print("保存前")
    # user.save()
    # print("保存后")
    # return HttpResponse("ok")
    pass


def video(request,*args,**kwargs):
    video_list=models.Video.objects.all()
    level_list=models.Level.objects.all()
    cerogy_list=models.Category.objects.all()
    print(kwargs)
    filter_dic={}
    for k,v in kwargs.items():
        if str(v) !="0":
            filter_dic[k]=v


    fin_video_list=video_list.filter(**filter_dic)
    return render(request,"video.html",{"video_list":fin_video_list,"kwargs":kwargs,"level_list":level_list, \
                                        "cegory_list":cerogy_list

                                        })

def video2(request,*args,**kwargs):
    dr_id=kwargs.get("dr_id")
    cg_id=kwargs.get("cg_id")
    lv_id=kwargs.get("lv_id")
    direction_list=models.Direction.objects.all()
    level_list=models.Level.objects.all()
    print(type(dr_id))
    filter={}
    if dr_id=="0":
        #无方向
        cogray_list = models.Category.objects.filter()
        if cg_id=="0":
            #无分类
            pass
        else:
            filter["cg_id"]=cg_id
    else:
        cogray_list=models.Category.objects.filter(direction=dr_id)
        temp=cogray_list.values_list("id")
        cg_id_list=list(zip(*temp))[0]
        print("cg_id_list",cg_id,cg_id_list)
        if cg_id=="0":
            filter["cg_id__in"] = cg_id_list
        else:
            if int(cg_id) in cg_id_list:

                filter["cg_id"] = cg_id
            else:
                pass

    if lv_id!="0":
        print("pass")
        filter["lv_id"]=lv_id

    print("filter",filter)
    result_video=models.Video.objects.filter(**filter)
    print("result",result_video)

    return render(request,"video2.html",{"video_list":result_video,
                                         "direction_list":direction_list,
                                         "cogray_list":cogray_list,
                                         "level_list":level_list,
                                         "kwargs":kwargs,
                                         })

def editor(request):
    return render(request,"editor.html")


