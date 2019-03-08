from django.shortcuts import render,HttpResponse,redirect
from crm import form,models
import random,string,os
from django.db import IntegrityError
from django.core.cache import cache
from PerfectCRM import settings
# Create your views here.
def index(request):
    c=models.Customer.objects.select_related("consultant").query
    print("c",c)
    return render(request,"index.html")


def customer_list(request):
    return render(request,"sales/customer.html")

def enrollment(request,customer_id):
    customer_obj=models.Customer.objects.get(id=customer_id)
    random_str = "".join(random.sample(string.ascii_lowercase + string.digits, 8))

    msgs={}

    if request.method=="POST":

        model_form=form.EnrollmentModel(request.POST)

        if model_form.is_valid():
            msg = '''请将此链接发送给客户进行填写:
                            http://localhost:8000/crm/customer/registration/{enroll_obj_id}/{random_str}/'''
            try:

                model_form.cleaned_data["customer"] = customer_obj
                print("model_form_clean)",model_form.cleaned_data)
                #enroll_obj=models.Enrollment.objects.create(**model_form.cleaned_data)#虽然会创建失败，但会增加id
                enroll_obj = models.Enrollment(**model_form.cleaned_data)
                enroll_obj.save()#虽然会创建失败，但会增加id
                #print("enroll_obj.id", enroll_obj.id)
                cache.set(enroll_obj.id, random_str, 30000)
                msgs["msg"]=msg.format(enroll_obj_id=enroll_obj.id,random_str=random_str)

            except IntegrityError as e:
                enroll_obj = models.Enrollment.objects.get(customer_id=customer_obj.id,
                                                           enrolled_class_id=model_form.cleaned_data[
                                                               "enrolled_class"].id)

                if enroll_obj.contract_agreed:
                    return redirect("/crm/contract_review/%s/" % enroll_obj.id)
                model_form.add_error("__all__", "obj  aleardy exist")
                cache.set(enroll_obj.id, random_str, 30000)

                msgs["msg"] = msg.format(enroll_obj_id=enroll_obj.id,random_str=random_str)

    else:
        model_form=form.EnrollmentModel()

    return render(request,"sales/enrollment.html",{"modelobj":model_form,"customer":customer_obj,"msgs":msgs})

def registre(request,enrollment_id,random_str):
    if True:#cache.get(enrollment_id)==random_str:
        enroll_obj = models.Enrollment.objects.get(id=enrollment_id)
        status=0

        if request.method=="POST":
            if request.is_ajax():
                # print("ajax post", request.FILES)
                enroll_data_dir="%s/%s"%(settings.ENROLLED_DATA,enrollment_id)
                if not os.path.exists(enroll_data_dir):
                    os.makedirs(enroll_data_dir,exist_ok=True)
                for file_index,file_obj in request.FILES.items():
                    with open("%s/%s"%(enroll_data_dir,file_obj.name),"wb") as f:
                        for chunk in file_obj.chunks():
                            f.write(chunk)
            customer_obj = form.CustomerModel(request.POST,instance=enroll_obj.customer)

            if customer_obj.is_valid():

                customer_obj.save()
                enroll_obj.contract_agreed=True
                enroll_obj.save()
                status=1
                return render(request, "sales/enroll_registration.html",
                              {"status": status})



        else:
            if enroll_obj.contract_agreed:
                status=1

            customer_obj=form.CustomerModel(instance=enroll_obj.customer)

        return render(request,"sales/enroll_registration.html",{"customer_obj":customer_obj,"enroll_obj":enroll_obj,"status":status})
    else:
        return HttpResponse("链接已失效")

def contact_review(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)
    customermodel=form.CustomerModel(instance=enroll_obj.customer)
    enrollmodel=form.EnrollmentModel(instance=enroll_obj)

    return render(request,"sales/contract_review.html",{"enroll_obj":enroll_obj,"customerform":customermodel,"enrollform":enrollmodel})

def enrollment_rejection(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)
    enroll_obj.contract_agreed=False
    enroll_obj.save()
    return redirect("/crm/customer/%s/enrollment/"%(enroll_obj.customer.id))

def payment(request,enroll_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    errors=[]
    if request.method=="POST":
        payment_amount=request.POST.get("amount")
        if payment_amount:
            if int(payment_amount)<500:
                errors.append("缴费金额低于500元")
            else:
                payment_obj = models.Payment.objects.create(
                    customer=enroll_obj.customer,
                    course=enroll_obj.enrolled_class.course,
                    amount=payment_amount,
                    consultant=enroll_obj.consultant
                )
                payment_obj.save()
                enroll_obj.contract_approved=True
                enroll_obj.save()
                enroll_obj.customer.status=0
                enroll_obj.customer.save()
                return redirect("/king_admin/crm/customer/")
        else:
            errors.append("缴费金额低于500元")






    return render(request,"sales/payment.html",{"enroll_obj":enroll_obj,"errors":errors})