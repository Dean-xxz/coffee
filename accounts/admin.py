from django.contrib import admin
from .models import Wechat_user,Invitation,Shopping_cart,Coupon_bank,Notice

# Register your models here.


class Wechat_userAdmin(admin.ModelAdmin):
    list_display = ('id','nickname','create_time','headimgurl')
    search_fields = ('id','nickname')


admin.site.register(Wechat_user,Wechat_userAdmin)

class Shopping_cartAdmin(admin.ModelAdmin):
    list_display = ('user','product','is_active')

admin.site.register(Shopping_cart,Shopping_cartAdmin)

#class Coffee_bankAdmin(admin.ModelAdmin):
#    list_display = ('user','access_code','is_active')

#admin.site.register(Coffee_bank,Coffee_bankAdmin)


class Coupon_bankAdmin(admin.ModelAdmin):
    list_display = ('user','coupon','dead_line','is_active')


admin.site.register(Coupon_bank,Coupon_bankAdmin)

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('user','text','is_read')
    list_filter = ('is_read',)

admin.site.register(Notice,NoticeAdmin)
