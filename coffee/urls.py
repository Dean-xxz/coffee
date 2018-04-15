from django.contrib import admin
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ad/', include('ad.urls', namespace="ad")),   # 广告模块接口url
    url(r'^product/', include('product.urls', namespace="product")),  # 产品模块接口url
    url(r'^payment/', include('payment.urls', namespace="payment")),  # 支付模块接口url
    url(r'^formula/', include('formula.urls', namespace="formula")),  # 配方模块接口url
    url(r'^code/', include('access_code.urls', namespace="code")),  # 取货模块接口url
    url(r'^machine/', include('machine.urls', namespace="machine")),  # 机器模块接口url
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),  # 用户模块接口url

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
