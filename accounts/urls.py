import accounts.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^user/create/$', accounts.apis.create_user_api, name="user_create_api"),
    url(r'^openid/query/$', accounts.apis.query_openid_api, name="openid_query_api"),
]

