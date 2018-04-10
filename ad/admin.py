from django.contrib import admin
from .models import Advertisement

# Register your models here.

admin.site.site_header = "众咖科技集成管理平台"


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('order','link','image','is_terminal','video')
    list_filter = ('is_terminal',)


admin.site.register(Advertisement,AdvertisementAdmin)
