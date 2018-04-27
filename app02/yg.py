from newadmin.service import v1
from app02 import models

# class YinGunUserInfo(v1.BaseYinGunAdmin):
#     pass
#
# v1.site.register(models.UserInfo,YinGunUserInfo)

class YinGunXX(v1.BaseYinGunAdmin):
    list_display = ["id","title"]

v1.site.register(models.XX,YinGunXX)
v1.site.register(models.OO)
