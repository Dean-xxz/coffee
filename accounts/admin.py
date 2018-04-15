from django.contrib import admin
from .models import Wechat_user,Invitation,Shopping_cart,Coffee_bank

# Register your models here.


class Wechat_userAdmin(admin.ModelAdmin):
    list_display = ('id','nickname','create_time','headimgurl')
    search_fields = ('id','nickname')


admin.site.register(Wechat_user,Wechat_userAdmin)

class Shopping_cartAdmin(admin.ModelAdmin):
    list_display = ('user','product','is_active')

admin.site.register(Shopping_cart,Shopping_cartAdmin)

class Coffee_bankAdmin(admin.ModelAdmin):
    list_display = ('user','access_code','is_active')

admin.site.register(Coffee_bank,Coffee_bankAdmin)


