
from django.shortcuts import render,HttpResponse
from crm.permission.permission_list import permission_dict
from django.core.urlresolvers import resolve
# 'can_access_my_course': {
#     "url": "my_class",
#     "url_type": "0",
#     "method": "GET",
#     "args": []
#
# },
def check_perm(*args,**kwargs):
    request=args[0]
    request_url=args[0].path
    print(request_url)
    if request.user.is_authenticated():
        for k,permission in permission_dict.items():
            url_match=False
            if permission["url_type"]=="1":
                if permission["url"]==request_url:
                    url_match=True
            else:
                url=resolve(request_url)

                if url.url_name==permission["url"]:
                    url_match=True


            if url_match:
                print("url_match", url_match)
                if request.method==permission["method"]:
                    arg_match=True
                    for request_arg in permission["args"]:
                        request_method_func=getattr(request,permission)
                        if not request_method_func.get(request_arg):
                            arg_match=False

                    if arg_match:

                        #在这里使用定义好的函数，进行业务逻辑内的判断
                        print("arg match")
                        if request.user.has_perm(k):
                            print("有权限")
                            return True





    return False
def check_permission(func):
    def inner(*args,**kwargs):
        if check_perm(*args,**kwargs):

            return func(*args,**kwargs)
        else:
            return HttpResponse("对不起，你没权限")
    return inner
