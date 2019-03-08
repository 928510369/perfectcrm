from django.contrib import admin
from app01.models import *
from app01 import models
# Register your models here.
class MyAdmin(admin.ModelAdmin):
    list_display = ("title","price","page_num",)
    search_fields = ("title",)
    list_filter = ("title",)
    ordering =("-id",)

class VideoAdmin(admin.ModelAdmin):
    list_display = ("id","lv_id","cg_id","title")
admin.site.register(Author)
admin.site.register(Book,MyAdmin)

admin.site.register(Video,VideoAdmin)
admin.site.register(Level)
admin.site.register(Direction)
admin.site.register(Category)