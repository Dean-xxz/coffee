#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 支付模块所需公共api
"""
import json
from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI
from django.views.generic import View
from .models import Order,Wechat_Transcation
from product.models import Product
from .wx_pay_utils import build_form_by_params
from .pay_settings import ALI_PAY_CONFIG

config = ALI_PAY_CONFIG

# 创建订单
from alipay import AliPay, ISVAliPay
#
app_private_key_string = open("/home/coffee/coffee/payment/ali_key/rsa_private_key.pem").read()
alipay_public_key_string = open("/home/coffee/coffee/payment/ali_key/rsa_public_key.pem").read()

alipay = AliPay(
#    appid=config['alipay_partner'],
    appid='2018011201807222',
    app_notify_url=config['alipay_notify_url'],  # 默认回调url
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    sign_type="RSA", # RSA 或者 RSA2
    debug=True  # 默认False
)



class OrderCreationAPI(AbstractAPI):
    def config_args(self):
        self.args = {
                'product_id': 'r',
                'channel':'r',
                }
    def access_db(self, kwarg):
        product_id = kwarg['product_id']
        channel = kwarg['channel']

        if channel == 'W':
            try:
                product = Product.objects.get(pk = product_id)
                total_fee = int(product.vip_price)
                body = product.title.encode('utf-8')

                order = Order(product_id = product_id,total_fee = total_fee,channel = channel)
                order.save()
                out_trade_no = order.id
                # Payment
                params = build_form_by_params({
                    'body': body,
                    'out_trade_no': out_trade_no,
                    'total_fee': '1',
                    'spbill_create_ip': '121.201.67.209',
                    # 'openid': 'oVXUA5fx9QbbEFL9hswQNS3F9W1Y',
                })
                print (app_private_key_string)
                data = json.dumps(params)
                # data = order.get_json()

                return data

            except Product.DoesNotExist:
                return None

        if channel == 'Z':
            try:
                product = Product.objects.get(pk=product_id)
                total_fee = int(product.vip_price)
                body = product.title.encode('utf-8')

                order = Order(product_id=product_id, total_fee=total_fee, channel=channel)
                order.save()
                tn = order.id
                subject = '众咖科技现磨咖啡'
                # Payment
                # params = create_direct_pay_by_user(tn = tn, subject = subject, body = body, total_fee = total_fee)

                # data = json.dumps(params)
                # data = order.get_json()
                data=alipay.api_alipay_trade_precreate(subject="test subject",out_trade_no=tn,total_amount=1)
                return data

            except Product.DoesNotExist:
                return None

    def format_data(self, data):
        if data is not None:
            return ok_json(data=data)
        return fail_json('订单创建失败')

create_order_api = OrderCreationAPI().wrap_func()


# 接受回调并更改订单状态


class NotifyView(View):
    def post(self, request, *args, **kwargs):
        order_id = request.POST['out_trade_no']
        info = {
            "order":order_id
        }
        print (info)
        print ('wakakakakakaa')
        return ok_json(data = info)
