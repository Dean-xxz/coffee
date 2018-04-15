from django.contrib import admin
from .models import Coupon

# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ('title','dead_line','type')
    list_filter = ('type',)


admin.site.register(Coupon,CouponAdmin)

