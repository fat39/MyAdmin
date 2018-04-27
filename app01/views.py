# from django.urls import reverse
#
# from django.shortcuts import render,HttpResponse
# from app01 import models
#
# def index(request):
#     ''' 访问初始页，添加数据 '''
#     user_group_list = models.UserGroup.objects.all()
#     context = {
#         "user_group_list":user_group_list
#     }
#     return render(request,"test.html",context)
#
# def add_test(request):
#     """ FK的添加页面，可以使popup的，也可以使正常的 """
#     if request.method == "GET":
#         return render(request,"add_test.html")
#     else:
#         popid = request.GET.get("popup")
#         if popid:
#             # 通过popup新创建一个页面
#             title = request.POST.get("title")
#             obj = models.UserGroup.objects.create(title=title)
#             # response = {"id":obj.id,"title":obj.title}
#             # 1.关闭popup页面
#             # 2.将新增数据添加，传送到原来发送pop页面中的ugID标签位置 popid=popID
#             context = {
#                 "data_dict":{"pk":obj.pk,"text":obj.title,"popid":popid}
#             }
#             return render(request,"popup_response.html",context)
#         else:
#             # 正常操作
#             title = request.POST.get("title")
#             models.UserGroup.objects.create(title=title)
#             return HttpResponse("列表页面：所有")