import accounts.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^user/create/$', accounts.apis.create_user_api, name="user_create_api"),
    url(r'^openid/query/$', accounts.apis.query_openid_api, name="openid_query_api"),
    url(r'^cart/create/$', accounts.apis.create_cart_api, name="cart_create_api"),
    url(r'^cart/delete/$', accounts.apis.delete_cart_api, name="cart_delete_api"),    
    url(r'^cart/list/$', accounts.apis.list_cart_api, name="cart_list_api"),
    url(r'^bank/create/$', accounts.apis.create_bank_api, name="bank_create_api"),
    url(r'^bank/update/$', accounts.apis.update_bank_api, name="bank_update_api"),
    url(r'^bank/list/$', accounts.apis.list_bank_api, name="bank_list_api"),
    url(r'^order/list/$', accounts.apis.list_order_api, name="order_list_api"),
    url(r'^coupon/list/$', accounts.apis.list_coupon_api, name="coupon_list_api"),
    url(r'^mycoupon/create/$', accounts.apis.create_mycoupon_api, name="mycoupon_create_api"),
    url(r'^mycoupon/list/$', accounts.apis.list_mycoupon_api, name="mycoupon_list_api"),

]

