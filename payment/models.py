import json
from django.db import models
from utils.basemodel.base import BaseModel
from django.core import serializers
from product.models import Product

# Create your models here.

class Order(BaseModel):

    """
    支付系统订单表，外键关联产品表Product
    """
    CHANNEL_CHOICES = (
            ('Z',("支付宝支付")),
            ('W',("微信支付")),
        )
    # user
    product = models.ForeignKey("product.Product",verbose_name = "产品",related_name = "order_product")
    total_fee = models.DecimalField(max_digits = 10,decimal_places = 2,verbose_name="总价")
    channel = models.CharField(max_length = 1,verbose_name = "支付渠道",null = True,blank = True,choices = CHANNEL_CHOICES)
    is_payment = models.BooleanField(verbose_name="是否付款",default=False)
    is_delivery =models.BooleanField(verbose_name="是否发货",default=False)
    is_refound = models.BooleanField(verbose_name="是否退款",default=False)
    # coupon
    remarks = models.CharField(max_length=1024,verbose_name="备注",null=True,blank=True)


    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"
        ordering = ["-update_time",]

    # def __str__(self):
    #     return self.product

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


class Wechat_Transcation(BaseModel):

    """
    微信支付表
    """

    openid = models.CharField(max_length=128,verbose_name="用户唯一身份标识",null=True,blank=True)
    order = models.ForeignKey("Order",verbose_name='订单',related_name ='wechat_order')
    trade_type = models.CharField(max_length=16,verbose_name='支付类型',help_text="JSAPI:公众号支付,NATIVE: 扫码支付,APP:APP支付")
    total_fee = models.DecimalField(max_digits = 10,decimal_places = 2,verbose_name="总价")
    nonce_str = models.CharField(max_length=32,verbose_name="随机字符串")
    return_code = models.CharField(max_length=24,verbose_name="返回码")
    result_code = models.CharField(max_length=24,verbose_name="结果码")
    mch_id = models.CharField(max_length=32,verbose_name="商户id")
    appis = models.CharField(max_length=32,verbose_name="公众号id")
    time_end = models.CharField(max_length=64,verbose_name="交易截止时间")
    sign = models.CharField(max_length=128,verbose_name="签名")
    product_id = models.IntegerField(verbose_name="商品id")


    class Meta:
        verbose_name = "微信订单"
        verbose_name_plural = "微信订单"
        ordering = ["-update_time",]

    def __str__(self):
        return self.order

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data

