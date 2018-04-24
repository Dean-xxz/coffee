from django.contrib import admin
from .models import Order,Wechat_Transcation

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('scene','machine','total_fee','user','channel','is_payment','update_time')
    list_filter = ('is_payment','channel','scene',)
    search_fields = ('id',)


admin.site.register(Order,OrderAdmin)


