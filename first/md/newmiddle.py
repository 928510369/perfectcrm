# from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            #执行当前中间件的process_request方法
            response = self.process_request(request)
        if not response:
            # 执行下一个中间件的call方法
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            # 执行当前中间件的process_response方法
            response = self.process_response(request, response)
        return response
class Agou(MiddlewareMixin):
    def process_request(self,request):
        print("阿狗req")


    def process_view(self,request,view_func,view_func_args,view_func_kwargs):
        print("阿狗process_view")
    def process_exception(self,request,exception):
        print("阿狗process_exception")

    def process_response(self,request,response):
        print("是sb")

        return response


class Shaniu(MiddlewareMixin):
    def process_request(self,request):
        print("shaniu req")


    def process_view(self, request, view_func, view_args, view_kwargs):
        print("傻妞process_view")

    def process_exception(self, request, exception):
        print("傻妞process_exception")

    def process_response(self,request,response):
        print("是222")
        return response
        # return HttpResponse("ok123")
