from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
register=template.Library()

@register.simple_tag
def render_level_a(level_obj,arg_dict):

    url=reverse("video",kwargs={"lv_id":level_obj.id,"cg_id":arg_dict.get("cg_id")})
    print("url",url)

    if str(level_obj.id)==arg_dict.get("lv_id"):
        a_ele=" <a class='red' href=%s>%s</a>"%(url,level_obj.name)
    else:
        a_ele = " <a  href=%s>%s</a>" % (url, level_obj.name)
    return mark_safe(a_ele)


@register.simple_tag
def render_cegory_a(cegory_obj,arg_dict):
    url = reverse("video", kwargs={"lv_id": arg_dict.get("lv_id"), "cg_id": cegory_obj.id})

    print("url",url)

    if str(cegory_obj.id)==arg_dict.get("cg_id"):
        a_ele=" <a class='red' href=%s>%s</a>"%(url,cegory_obj.name)
    else:
        a_ele = " <a  href=%s>%s</a>" % (url, cegory_obj.name)
    return mark_safe(a_ele)

@register.simple_tag
def render_total_a(arg_dict,key):
    if key=="lv_id":
        url = reverse("video", kwargs={"lv_id": 0, "cg_id": arg_dict.get("cg_id")})
        a_ele=" <a  href=%s>%s</a>"%(url,"全部")
    else:
        url = reverse("video", kwargs={"lv_id":arg_dict.get("lv_id"), "cg_id":0})
        a_ele = " <a  href=%s>%s</a>" % (url, "全部")
    return mark_safe(a_ele)

########
@register.simple_tag
def render_direction_a(direction,args_dict):

    url = reverse("video2", kwargs={"dr_id":direction.id,"lv_id":args_dict.get("lv_id"), "cg_id":args_dict.get("cg_id")})

    print("url", url)

    if str(direction.id) == args_dict.get("dr_id"):
        a_ele = " <a class='red' href=%s>%s</a>" % (url,direction.name)
    else:
        a_ele = " <a  href=%s>%s</a>" % (url, direction.name)
    return mark_safe(a_ele)


@register.simple_tag
def render_level2_a(level_obj,args_dict):

    url=reverse("video2",kwargs={"dr_id":args_dict.get("dr_id"),"lv_id":level_obj.id,"cg_id":args_dict.get("cg_id")})
    print("url",url)

    if str(level_obj.id)==args_dict.get("lv_id"):
        a_ele=" <a class='red' href=%s>%s</a>"%(url,level_obj.name)
    else:
        a_ele = " <a  href=%s>%s</a>" % (url, level_obj.name)
    return mark_safe(a_ele)


@register.simple_tag
def render_cegory2_a(cegory_obj,args_dict):
    url = reverse("video2", kwargs={"dr_id":args_dict.get("dr_id"),"lv_id":args_dict.get("lv_id"),"cg_id": cegory_obj.id})

    print("url",url)

    if str(cegory_obj.id)==args_dict.get("cg_id"):
        a_ele=" <a class='red' href=%s>%s</a>"%(url,cegory_obj.name)
    else:
        a_ele = " <a  href=%s>%s</a>" % (url, cegory_obj.name)
    return mark_safe(a_ele)


@register.simple_tag
def render_total2_a(args_dict,key):
    if key=="lv_id":
        url = reverse("video2", kwargs={"dr_id":args_dict.get("dr_id"),"lv_id": 0, "cg_id": args_dict.get("cg_id")})

    elif key=="cg_id":
        url = reverse("video2", kwargs={"dr_id":args_dict.get("dr_id"),"lv_id":args_dict.get("lv_id"), "cg_id":0})

    elif key=="dr_id":
        url = reverse("video2", kwargs={"dr_id": 0, "lv_id": args_dict.get("lv_id"), "cg_id":args_dict.get("cg_id")})
    else:
        url=""

    if args_dict.get(key)=="0":
        a_ele = " <a class='red' href=%s>全部</a>" % (url)
    else:
        a_ele = " <a  href=%s>全部</a>" % (url)
    return mark_safe(a_ele)