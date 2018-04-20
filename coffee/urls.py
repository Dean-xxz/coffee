from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from accounts.apis import CodeView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ad/', include('ad.urls', namespace="ad")),   # 广告模块接口url
    url(r'^product/', include('product.urls', namespace="product")),  # 产品模块接口url
    url(r'^payment/', include('payment.urls', namespace="payment")),  # 支付模块接口url
    url(r'^formula/', include('formula.urls', namespace="formula")),  # 配方模块接口url
    url(r'^code/', include('access_code.urls', namespace="code")),  # 取货模块接口url
    url(r'^machine/', include('machine.urls', namespace="machine")),  # 机器模块接口url
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),  # 用户模块接口url
    url(r'^wechat/oauth$', CodeView.as_view(), name="wechat_oauth_api"),
    url(r'^wechat/oauth/MP_verify_dEL3zvMhlfiUJgmt\.txt',TemplateView.as_view(template_name= 'MP_verify_dEL3zvMhlfiUJgmt.txt')),
    url(r'',TemplateView.as_view(template_name="index.html"),name="index")

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
