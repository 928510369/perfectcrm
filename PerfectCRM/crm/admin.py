from django.contrib import admin
from crm import models
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from  django.shortcuts import redirect,render,HttpResponse
# Register your models here.

class CustomersAdmin(admin.ModelAdmin):
    list_display = ('id','name','qq','source','consultant','content','status','date',)
    list_filter = ('consultant','source','consultant','date')
    search_fields = ('qq','name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',"consultant")

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name',)


class CourseRecordAdmin(admin.ModelAdmin):
    list_display = ("from_class","day_num","teacher","has_homework","homework_title","homework_content","outline")

    search_fields = ('from_class', 'day_num')

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
            return redirect("/admin/crm/studyrecord/?course_record__id__exact=%s"%(queryset[0].day_num))
        except Exception as e:
            return HttpResponse("学习记录已存在，不可重复创建")




    initialize_studyrecord.short_description = "初始化本课程的学习记录"


class StudyRecordAdmin(admin.ModelAdmin):
    list_display =("student","course_record","attendance","score")
    list_filter = ("course_record","student__customer__qq")
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin',"is_active")
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',"is_active","stu_account","roles","user_permissions","groups")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ("user_permissions","groups")
admin.site.register(models.UserProfile, UserAdmin)
admin.site.register(models.Customer,CustomersAdmin)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Enrollment)
admin.site.register(models.Course)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord,CourseRecordAdmin)
admin.site.register(models.Branch)
admin.site.register(models.Role)
admin.site.register(models.Payment)
admin.site.register(models.StudyRecord,StudyRecordAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Contract)
#admin.site.register(models.UserProfile)
admin.site.register(models.Menu)

