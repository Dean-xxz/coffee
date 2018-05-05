import coupon.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^couponbank/create/$', coupon.apis.create_couponbank_api, name="couponbank_create_api"),
    url(r'^couponbank/list/$', coupon.apis.list_couponbank_api, name="couponbank_list_api"),

]
