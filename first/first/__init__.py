# from django.db.models.signals import pre_save,post_save#使用信号量对model进行监控
# import django.dispatch
# def callback(*args,**kwargs):
#     print("model保存前")
#
# def callback1(*args,**kwargs):
#     print("model保存后")
#
# def callback2(*args,**kwargs):
#     print("自定义信号量1")
# def callback3(*args,**kwargs):
#     print("自定义信号量2")
# pre_save.connect(callback)
#
# post_save.connect(callback1)
#
# mysignal=django.dispatch.Signal(providing_args=["name"])
# mysignal.connect(callback2)
# mysignal.connect(callback3)