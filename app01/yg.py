from newadmin.service import v1
from app01 import models
from django.utils.safestring import mark_safe
from django.urls import reverse


class YinGunUserInfo(v1.BaseYinGunAdmin):

    def func(self,obj=None,is_header=False):
        if is_header:
            return "操作"
        # name = "{0}:{1}_{2}_change".format(self.site.namespace,self.model_class._meta.app_label,self.model_class._meta.model_name)
        # url = reverse(name,args=(obj.pk,))

        from django.http.request import QueryDict
        param_dict = QueryDict(mutable=True)
        if self.request.GET:
            param_dict["_changelistfilter"] = self.request.GET.urlencode()

        base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label,self.model_name,self.site.namespace),args=(obj.pk,))
        edit_url = "{0}?{1}".format(base_edit_url,param_dict.urlencode())

        base_delete_url = reverse("{2}:{0}_{1}_delete".format(self.app_label,self.model_name,self.site.namespace),args=(obj.pk,))
        delete_url = "{0}?{1}".format(base_delete_url, param_dict.urlencode())

        return mark_safe("<a href='{0}'>编辑</a>|<a href='{1}'>删除</a>".format(edit_url,delete_url))

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return mark_safe("<input type='checkbox' />")

        tag = "<input name='pk' type='checkbox' value='{0}' />".format(obj.pk)
        return mark_safe(tag)

    def comb(self,obj=None,is_header=False):
        if is_header:
            return "某列"

        return "%s-%s" % (obj.username,obj.email)


    def initial(self,request):
        pk_list = request.POST.getlist("pk")
        # print(pk_list)
        models.UserInfo.objects.filter(pk__in=pk_list).update(username="adfsdf")
        return True


    def multiply_del(self,request):
        pass
    initial.text = "初始化"
    multiply_del.text = "批量删除"

    list_display = [checkbox,"id","username","email","ug",comb,func]
    action_list = [initial,multiply_del,]

    from newadmin.utils.filter_code import FilterOption

    def email(self,option,request):
        from newadmin.utils.filter_code import FilterList
        queryset = models.UserInfo.objects.filter(id__gt=2)
        return FilterList(option,queryset,request)

    filter_list = [
        FilterOption("username",False,text_func_name="text_username",val_func_name="value_username"),
        FilterOption(email,False,text_func_name="text_email",val_func_name="value_email"),
        # FilterOption("email",False,text_func_name="text_email",val_func_name="value_email"),
        FilterOption("ug",True),
        FilterOption("role",True),
    ]
    # 1.取数据，放在页面上？
    # username -> UserInfo表
    # ug -> UserGroup表
    # role -> Role表
    # 2.单选和多选自己定义
    # request.GET   {}



class YinGunRole(v1.BaseYinGunAdmin):
    list_display = ["id","name"]



class YinGunUserGroup(v1.BaseYinGunAdmin):

    def func(self,obj=None,is_header=False):
        if is_header:
            return "操作"
        # name = "{0}:{1}_{2}_change".format(self.site.namespace,self.model_class._meta.app_label,self.model_class._meta.model_name)
        # url = reverse(name,args=(obj.pk,))

        from django.http.request import QueryDict
        param_dict = QueryDict(mutable=True)
        if self.request.GET:
            param_dict["_changelistfilter"] = self.request.GET.urlencode()

        base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label,self.model_name,self.site.namespace),args=(obj.pk,))
        edit_url = "{0}?{1}".format(base_edit_url,param_dict.urlencode())

        base_delete_url = reverse("{2}:{0}_{1}_delete".format(self.app_label,self.model_name,self.site.namespace),args=(obj.pk,))
        delete_url = "{0}?{1}".format(base_delete_url, param_dict.urlencode())

        return mark_safe("<a href='{0}'>编辑</a>|<a href='{1}'>删除</a>".format(edit_url,delete_url))

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return mark_safe("<input type='checkbox' />")

        tag = "<input type='checkbox' value='{0}' />".format(obj.pk)
        return mark_safe(tag)


    list_display = [checkbox,"id","title",func]

v1.site.register(models.UserInfo,YinGunUserInfo)
v1.site.register(models.Role,YinGunRole)
v1.site.register(models.UserGroup,YinGunUserGroup)
