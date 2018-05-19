import payment.apis
import payment.js_apis
import payment.crm_apis
from django.conf.urls import url
from .apis import NotifyView,payment_wxnotify_view

urlpatterns = [
    url(r'^order/create/$', payment.apis.create_order_api, name="order_create_api"),
    url(r'^notify/$', payment.apis.NotifyView.as_view(), name="payment_notify_api"),
    url(r'^wxnotify/$', payment_wxnotify_view, name="payment_wxnotify_api"),
    url(r'^order/query/$', payment.apis.query_order_api, name="order_query_api"),
    url(r'^market/order/create/$', payment.js_apis.create_order_api, name="market_order_create_api"),
    #销售系统
    url(r'^crm/mch/list/$', payment.crm_apis.list_sale_api, name="sale_list_api"),
    url(r'^crm/machine_sales/list/$', payment.crm_apis.list_machine_sale_api, name="machine_sale_list_api"),
    url(r'^crm/machine/list/$', payment.crm_apis.list_machine_api, name="machine_list_api"),
    url(r'^crm/machine/count/$', payment.crm_apis.count_machine_api, name="machine_count_api"),
    url(r'^crm/machine/error/list/$', payment.crm_apis.list_machineerror_api, name="machineerror_list__api"),
    url(r'^crm/machine/material/list/$', payment.crm_apis.list_machinematerial_api, name="machinematerial_list__api"),
    url(r'^crm/machine/error/query/$', payment.crm_apis.query_error_api, name="error_query__api"),
    url(r'^crm/machine/material/query/$', payment.crm_apis.query_material_api, name="material_query__api"),

]
