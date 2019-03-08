from django.shortcuts import render,HttpResponse
from PerfectCRM import settings
import os,json,time
from  crm import models
from crm.permission.permission import check_permission
# Create your views here.

@check_permission
def my_class(request):
    return render(request,"student/my_class.html")

def studyrecords(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)
    print("enroll_obj",enroll_obj)
    return render(request,"student/study_record.html",{"enroll_obj":enroll_obj})

def homework_detail(request,studyrecord_id):
    studyrecord_obj=models.StudyRecord.objects.get(id=studyrecord_id)
    homework_path = "{base_path}/{class_id}/{courserecord_id}/{studyrecord_id}/" \
        .format(base_path=settings.HOMEWORK_DATA, class_id=studyrecord_obj.student.enrolled_class.id,
                courserecord_id=studyrecord_obj.course_record.id, studyrecord_id=studyrecord_id)
    if request.method=="POST":
        print(request.FILES,studyrecord_obj.student.enrolled_class.id,studyrecord_obj.course_record.id,studyrecord_id)

        print(homework_path)
        if not os.path.isdir(homework_path):
            os.makedirs(homework_path,exist_ok=True)


        for k,file_obj in request.FILES.items():
            with open("%s/%s"%(homework_path,file_obj.name),"wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

    file_lists = []
    for file_name in os.listdir(homework_path):
        f_path = "%s/%s" % (homework_path, file_name)
        modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.stat(f_path).st_mtime))
        file_lists.append([file_name, os.stat(f_path).st_size, modify_time])







    return render(request,"student/homework_detail.html",{"studyrecord_obj":studyrecord_obj,'file_lists': file_lists})