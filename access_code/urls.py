import access_code.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^access_code/create/$', access_code.apis.create_code_api, name="code_create_api"),
    url(r'^access_code/update/$', access_code.apis.update_code_api, name="code_update_api"),
    url(r'^access_code/query/$', access_code.apis.query_code_api, name="code_query_api"),
    url(r'^code_info/query/$', access_code.apis.query_codeinfo_api, name="codeinfo_query_api"),
]
