# ('can_access_my_course','可以访问我的课程'),
#                        ('can_access_customer_list','可以访问客户列表'),
#                        ('can_access_customer_detail','可以访问客户详细'),
#                        ('can_access_studyrecords','可以访问学习记录页面'),
#                        ('can_access_homework_detail','可以访问作业详情页面'),
#                        ('can_upload_homework','可以交作业'),
#                        ('access_kingadmin_table_obj_detail','可以访问kingadmin每个表的对象'),
#                        ('change_kingadmin_table_obj_detail','可以修改kingadmin每个表的对象'),
#
# url_type 0代表相对，1代表绝对路径                )
permission_dict = {
    'crm.can_access_my_course': {
        "url": "my_class",
        "url_type": "0",
        "method": "GET",
        "args": [
            "course_select"

        ]

    },
    'crm.can_access_customer_list': {
        "url": "/king_admin/crm/customer/",
        "url_type": "1",
        "method": "GET",
        "args": []

    },
    'crm.can_access_customer_detail': {
        "url": "table_objs_change",
        "url_type": "0",
        "method": "GET",
        "args": []

    },
    'crm.can_access_studyrecords': {
        "url": "studyrecords",
        "url_type": "0",
        "method": "GET",
        "args": []

    },
    'crm.can_access_homework_detail': {
        "url": "homework_detail",
        "url_type": "0",
        "method": "GET",
        "args": []

    },
    'crm.can_upload_homework': {
        "url": "homework_detail",
        "url_type": "0",
        "method": "POST",
        "args": []
    },
    'crm.access_kingadmin_table_obj_detail': {
        "url": "table_objs_change",
        "url_type": "0",
        "method": "GET",
        "args": []

    },
    'crm.change_kingadmin_table_obj_detail': {
        "url": "table_objs_change",
        "url_type": "0",
        "method": "POST",
        "args": []

    },

}

def course_select():
    pass
