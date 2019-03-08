from django.forms import ModelForm
from django.forms import ValidationError
from django.utils.translation import ugettext as _
def create_model_form(request,modeladmin):

    def __new__(cls,*args,**kwargs):
        #print('cls',cls)#代指自身class

        for field_name,field_value in cls.base_fields.items():
            cls.base_fields[field_name].widget.attrs["class"]="form-control"
            if not hasattr(modeladmin,"is_add_form"):
                if field_name in modeladmin.readonly_fields:
                    cls.base_fields[field_name].widget.attrs["disabled"] = "disabled"
            if hasattr(modeladmin, "clean_%s" % field_name):
                field_clean_func = getattr(modeladmin, "clean_%s" % field_name)
                setattr(cls, "clean_%s" % field_name, field_clean_func)
        return ModelForm.__new__(cls)

    def default_clean(self):
        error_list = []
        if self.instance.id:
        # print("self",self)


            for field in modeladmin.readonly_fields:
                field_value=getattr(self.instance,field)

                field_val_from_front=self.cleaned_data.get(field)
                # print(field,field_value,field_val_from_front)
                print(field,field_val_from_front)
                if hasattr(field_value,"all"):
                    field_val_list=getattr(field_value,"all")().values_list("id")

                    m2m_id_list =set([i[0] for i in field_val_list])
                    print(m2m_id_list)
                    new_m2m_id_list= set([i.id for i in self.cleaned_data.get(field)])
                    if m2m_id_list!=new_m2m_id_list:
                        self.add_error(field,"%s readonly"%(field))
                    continue
                if field_value !=field_val_from_front:
                    error_list.append(ValidationError(_("readonly %(field)s must be %(val)s"),code="invalid",params={"field":field,"val":field_value}))
        self.ValidationError=ValidationError
        response=modeladmin.default_form_validation(self)
        if response:
            error_list.append(response)


        if error_list:

            raise ValidationError(error_list)
        if modeladmin.tablereadonly_option:
            raise ValidationError(
                _('Table is  readonly,cannot be modified or added'),
                code='invalid'
            )
    class Meta:
        model=modeladmin.model
        fields="__all__"
        exclude=modeladmin.modelform_exclude_fields


    attrs={"Meta":Meta}
    model_form_class=type("DynaticModelForm",(ModelForm,),attrs)
    setattr(model_form_class,"__new__",__new__)
    setattr(model_form_class, "clean",default_clean)
    return model_form_class