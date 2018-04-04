#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 支付模块所需公共api
"""
import json
from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI
from django.views.generic import View
from django.http import HttpResponse
from .models import Order,Wechat_Transcation
from product.models import Product,Item,Category
from .wx_pay_utils import build_form_by_params,notify_xml_string_to_dict,notify_success_xml,verify_notify_string
from .pay_settings import ALI_PAY_CONFIG

config = ALI_PAY_CONFIG

from alipay import AliPay, ISVAliPay


#初始化支付宝支付sdk
app_private_key_string = open("/home/coffee/coffee/payment/ali_key/rsa_private_key.pem").read()
alipay_public_key_string = open("/home/coffee/coffee/payment/ali_key/rsa_public_key.pem").read()

alipay = AliPay(
    appid=config['alipay_partner'],
    app_notify_url=config['alipay_notify_url'],  # 默认回调url
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    sign_type="RSA2", # RSA 或者 RSA2
    debug=False  # 默认False
)


 

#创建订单接口
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
                body = product.title

                order = Order(product_id = product_id,total_fee = total_fee,channel = channel)
                order.save()
                out_trade_no = order.id
                # Payment
                total_fee = total_fee*100
                params = build_form_by_params({
                    'body': body,
                    'out_trade_no': out_trade_no,
                    'total_fee': total_fee,
                    'spbill_create_ip': '121.201.67.209',
                })
                data = json.dumps(params)
                data = json.loads(data)
                data['out_trade_no'] = out_trade_no
                return data

            except Product.DoesNotExist:
                return None

        if channel == 'Z':
            try:
                product = Product.objects.get(pk=product_id)
                total_fee = int(product.vip_price)
                subject = product.title

                order = Order(product_id=product_id, total_fee=total_fee, channel=channel)
                order.save()
                tn = order.id
                data=alipay.api_alipay_trade_precreate(subject=subject,out_trade_no=tn,total_amount=total_fee)
               	print (data)
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
            #get password and username 
        order_id = request.POST['out_trade_no']
        status = request.POST['trade_status']
        if status=='TRADE_SUCCESS':
            order = Order.objects.filter(id = order_id).update(is_payment=True)
            return HttpResponse(
                        notify_success_xml(),
                        content_type='application/xml',
                     )
        #如果不成功，测取消订单
        return fail_json()


def payment_wxnotify_view(request):
    if verify_notify_string(request.body) is True:
    	notify = notify_xml_string_to_dict(request.body)
    	order_id = notify['out_trade_no']
    	order = Order.objects.filter(id = order_id).update(is_payment=True)
    	return HttpResponse(
        	        notify_success_xml(),
                	content_type='application/xml',
                     )
    return fail_json()	



# 订单结果查询接口
class OrderQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
                'order_id': 'r',
                }
    def access_db(self, kwarg):
        order_id = kwarg['order_id']
        try:
            order = Order.objects.get(pk = order_id,is_payment = True)
            product = order.product.get_json()
            item_ids = product['items']
            product['item_info'] = []
            for j in item_ids:
                item_detail = Item.objects.get(pk = j)
                item_detail = item_detail.get_json()
                item_detail.pop('update_time')
                item_detail.pop('create_time')
                item_detail.pop('is_active')
                category_id = item_detail['category']
                category = Category.objects.get(pk = category_id)
                item_detail['category'] = category.title
                product['item_info'].append(item_detail)
            product.pop('create_time')
            product.pop('update_time')
            product.pop('is_active')
            product.pop('items')
            data = product
            return data
        except Order.DoesNotExist:
            return None
    
    def format_data(self, data):
        if data is not None:
            return ok_json(data=data)
        return fail_json('payment faild')

query_order_api = OrderQueryAPI().wrap_func()
