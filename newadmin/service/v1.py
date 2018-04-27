# -*- coding:utf-8 -*-

import copy
from django.shortcuts import HttpResponse,render,redirect
from django.urls import reverse

class BaseYinGunAdmin(object):
    list_display = "__all__"
    # list_display = ["id","username","email"]\
    action_list = []

    filter_list = []

    add_or_edit_model_form = None

    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site
        self.request = None

        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name


    def get_add_or_edit_model_form(self):
        if self.add_or_edit_model_form:
            return self.add_or_edit_model_form
        else:
            from django.forms import ModelForm
            # class MyModelForm(ModelForm):
            #     class Meta:
            #         model = self.model_class
            #         fields = "__all__"
            _m = type("Meta",(object,),{"model":self.model_class,"fields":"__all__"})
            MyModelForm = type("MyModelForm",(ModelForm,),{"Meta":_m})
            return MyModelForm


    @property
    def urls(self):
        from django.urls import path,re_path,include
        info = self.model_class._meta.app_label,self.model_class._meta.model_name
        urlpatterns = [
            path('', self.changelist_view, name='%s_%s_changelist' % info),
            path('add/', self.add_view, name='%s_%s_add' % info),
            # path('<path:object_id>/delete/', self.delete_view, name='%s_%s_delete' % info),
            re_path('(\d+)/delete/', self.delete_view, name='%s_%s_delete' % info),
            # path('<path:object_id>/change/', self.change_view, name='%s_%s_change' % info),
            re_path('(\d+)/change/', self.change_view, name='%s_%s_change' % info),
        ]
        return urlpatterns

    def changelist_view(self,request):

        self.request = request
        # 生成页面上：添加按钮
        # namespace,app_label,model_name
        from django.http.request import QueryDict
        param_dict = QueryDict(mutable=True)
        if request.GET:
            param_dict["_changelistfilter"] = request.GET.urlencode()
        base_add_url = reverse("{2}:{0}_{1}_add".format(self.app_label,self.model_name,self.site.namespace))
        add_url = "{0}?{1}".format(base_add_url,param_dict.urlencode())


        # 分页开始
        from newadmin.utils.pager import PageInfo
        condition = {}
        result_list = self.model_class.objects.filter(**condition)
        base_page_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
        page_param_dict = copy.deepcopy(request.GET)
        page_param_dict._mutable = True
        page_obj = PageInfo(request.GET.get("page"),result_list.count(),base_page_url,page_param_dict)
        result_list = result_list[page_obj.start:page_obj.end]
        # 分页结束


        # action操作
        # get请求，显示下拉框
        action_list = []
        for item in self.action_list:
            tpl = {"name":item.__name__,"text":item.text}
            action_list.append(tpl)
        if request.method == "POST":
            # 1、获取action
            func_name_str = request.POST.get("action")
            ret = getattr(self,func_name_str)(request)
            action_page_url = reverse(
                "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
            if ret:
                action_page_url = "{0}?{1}".format(action_page_url,request.GET.urlencode())
            return redirect(action_page_url)

        ################# 组合搜索操作 #################

        from newadmin.utils.filter_code import FilterList
        filter_list = []
        for option in self.filter_list:
            if option.is_func:
                data_list = option.field_or_func(self,option,request)
            else:
                from django.db.models import ForeignKey,ManyToManyField,OneToOneField
                _field = self.model_class._meta.get_field(option.field_or_func)
                if isinstance(_field,OneToOneField):
                    # print(_field.related_model)
                    pass
                elif isinstance(_field,ForeignKey):
                    data_list = FilterList(option,_field.related_model.objects.all(),request)
                    # print(_field.related_model)    # ug
                elif isinstance(_field,ManyToManyField):
                    data_list = FilterList(option, _field.related_model.objects.all(), request)
                    # print(_field.related_model)  # role
                else:
                    data_list = FilterList(option, _field.model.objects.all(), request)
                    # print(_field.model)
            filter_list.append(data_list)

        context = {
            "result_list":result_list,
            "list_display":self.list_display,
            "ygadmin_obj":self,
            "add_url":add_url,
            "page_str":page_obj.pager(),
            "action_list":action_list,
            "filter_list":filter_list,
        }

        return render(request,"yg/change_list.html",context)


    def add_view(self,request):
        # print(request.GET.get("_changelistfilter"))
        if request.method == "GET":
            model_form_obj = self.get_add_or_edit_model_form()()
            context = {
                "form": model_form_obj,
            }

            return render(request, "yg/add.html", context)
        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST,files=request.FILES)
            if model_form_obj.is_valid():
                obj = model_form_obj.save()
                # 如果是popup
                popid = request.GET.get("popup")
                if popid:
                    # context = {
                    #     "pk":obj.pk,
                    #     "text":str(obj),
                    #     "popid":popid,
                    # }
                    context = {
                        "data_dict":{
                            "pk":obj.pk,
                            "text":str(obj),
                            "popid":popid,
                        }
                    }

                    return render(request,'yg/popup_response.html',context)
                else:
                    # 添加成功，进行跳转
                    base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
                    list_url = "{0}?{1}".format(base_list_url, request.GET.get("_changelistfilter"))
                    return redirect(list_url)
            context = {
                "form": model_form_obj,
            }

            return render(request, "yg/add.html", context)



    def delete_view(self,request,pk):
        """
        删除
        :param request:
        :param pk:
        :return:
        """
        '''
        根据pk获取数据，然后delete()
        # 获取url，跳转
        '''
        obj = self.model_class.objects.filter(pk=pk)
        if not obj:
            return HttpResponse("ID不存在")

        obj.delete()
        # 删除成功
        base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
        list_url = "{0}?{1}".format(base_list_url, request.GET.get("_changelistfilter"))
        return redirect(list_url)


    def change_view(self,request,pk):
        # 1.获取_changelistfilter中传递的参数
        # 2.页面显示并提供默认值ModelForm
        # 3.返回页面
        # request.GET.get("_changelistfilter")

        obj = self.model_class.objects.get(pk=pk)
        if not obj:
            return HttpResponse("ID不存在")

        if request.method == "GET":
            model_form_obj = self.get_add_or_edit_model_form()(instance=obj)
        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST,files=request.FILES,instance=obj)
            if model_form_obj.is_valid():
                model_form_obj.save()
                # 修改成功，进行跳转
                base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
                list_url = "{0}?{1}".format(base_list_url, request.GET.get("_changelistfilter"))
                return redirect(list_url)
        context = {
            "form":model_form_obj,
            # "model_class": self.model_class,
        }

        return render(request,"yg/edit.html",context)


class YinGunSite(object):
    def __init__(self):
        self._registry = {}
        self.namespace = "yingun"
        self.app_name = "yingun"

    def register(self,model_class,xxx=BaseYinGunAdmin):
        self._registry[model_class] = xxx(model_class,self)
        # print(self._registry)
        # {<class 'app01.models.UserInfo'>: <newadmin.service.v1.BaseYinGunAdmin object at 0x05F351F0>}

    def get_urls(self):
        from django.urls import re_path, include
        ret = [
            re_path("^login/",self.login,name="login"),
            # url("^logout/",self.logout,name="logout"),
        ]
        for model_cls,yingun_admin_obj in self._registry.items():
            app_label = model_cls._meta.app_label
            model_name = model_cls._meta.model_name
            # print(app_label,model_name)
            ret.append(re_path(r'^%s/%s/' % (app_label,model_name),include(yingun_admin_obj.urls)))
        return ret

    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.namespace

    def login(self,request):
        return HttpResponse("login")

    def logout(self,request):
        return HttpResponse("logout")


site = YinGunSite()
