from django.contrib import admin
from .models import Wechat_user,Invitation

# Register your models here.


class Wechat_userAdmin(admin.ModelAdmin):
    list_display = ('id','nickname','create_time','headimgurl')
    search_fields = ('id','nickname')


admin.site.register(Wechat_user,Wechat_userAdmin)


