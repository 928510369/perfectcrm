from django.shortcuts import render,redirect
from king_admin import king_admin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.util import filter_objs,sort_table,table_search
from django.contrib.auth import login,authenticate,logout
# Create your views here.
def acc_login(request):
    error = ""
    if request.method=="POST":
        _email=request.POST.get("email")
        _password=request.POST.get("password")
        user=authenticate(username=_email,password=_password)

        print(user)
        if user:
            login(request,user)
            next_url=request.GET.get("next","/")
            return redirect(next_url)
        else:
            error="wrong username and password"

    return render(request,"acc_login.html",{"error":error})

def log_out(request):

    logout(request)
    return redirect("/account/login/")

def index(request):
    return render(request,"index.html")