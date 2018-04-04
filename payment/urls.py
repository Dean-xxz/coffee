import payment.apis
from django.conf.urls import url
from .apis import NotifyView,payment_wxnotify_view

urlpatterns = [
    url(r'^order/create/$', payment.apis.create_order_api, name="order_create_api"),
    url(r'^notify/$', payment.apis.NotifyView.as_view(), name="payment_notify_api"),
    url(r'^wxnotify/$', payment_wxnotify_view, name="payment_wxnotify_api"),
    url(r'^order/query/$', payment.apis.query_order_api, name="order_query_api"),
]
