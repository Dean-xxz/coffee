import payment.apis
from django.conf.urls import url
from .apis import NotifyView

urlpatterns = [
    url(r'^order/create/$', payment.apis.create_order_api, name="order_create_api"),
    url(r'^notify/$', payment.apis.NotifyView.as_view(), name="payment_notify_api"),
]