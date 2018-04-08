from django.contrib import admin
from .models import Order,Wechat_Transcation

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product','machine','total_fee','channel','is_payment')
    list_filter = ('is_payment','channel',)
    search_fields = ('id',)


admin.site.register(Order,OrderAdmin)


