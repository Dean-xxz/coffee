import json
from django.db import models
from utils.basemodel.base import BaseModel
from django.core import serializers
from django.conf import settings
from product.models import Product
from coupon.models import Coupon
# Create your models here.

class Wechat_user(BaseModel):
    class Meta:

        verbose_name = "微信用户表"
        verbose_name_plural = "微信用户表"
        ordering = ["-create_time",]


    openid = models.CharField(max_length=50, blank=True, null=True, verbose_name=('OPENID'))
    unionid = models.CharField(max_length=50, verbose_name=('UNIONID'), unique=True,null = True,blank = True)
    nickname = models.CharField(max_length=50, verbose_name=('昵称'))
    sex = models.CharField(max_length=1, blank=True, null=True, verbose_name=('性别'))
    province = models.CharField(max_length=50, blank=True, null = True, verbose_name=('省份'))
    city = models.CharField(max_length=50, blank=True,null=True, verbose_name=('城市'))
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name=('国家'))
    headimgurl = models.URLField(blank=True,null=True,verbose_name=('头像'))
    language = models.CharField(max_length=10, blank=True, null=True, verbose_name=('语言'))
    privilege = models.CharField(max_length=50, blank=True, null=True, verbose_name=('特权用户'))

    def __str__(self):
        return self.nickname

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data



class Invitation(BaseModel):


    class Meta:
        verbose_name = "邀请表"
        verbose_name_plural = "邀请表"
        ordering = ["-create_time",]

    wechat_user = models.ForeignKey("Wechat_user",verbose_name="原用户",related_name="invitation_wechat_user")
    inviter = models.ForeignKey("Wechat_user",verbose_name="被邀请者",related_name="invitation_inviter")


    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data

class Shopping_cart(BaseModel):
    """
    购物车
    """
    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = "购物车"
        ordering = ["-create_time",]
    
    user = models.ForeignKey("Wechat_user",verbose_name="用户",related_name="cart_user")
    product = models.ForeignKey("product.Product",verbose_name="商品",related_name="cart_product")


    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


#class Coffee_bank(BaseModel):
    """
    咖啡库
    """
#    class Meta:
#        verbose_name = "咖啡库"
#        verbose_name_plural = "咖啡库"
#        ordering = ["-create_time",]

#    user = models.ForeignKey("Wechat_user",verbose_name="用户",related_name="coupon_user")
#    access_code = models.ForeignKey("access_code.Access_Code",verbose_name="提货码",related_name="bank_code")


#    def get_json(self):
#        serials = serializers.serialize("json", [self])
#        struct = json.loads(serials)
#        data = struct[0]['fields']
#        if 'pk' in struct[0]:
#            data['id'] = struct[0]['pk']
#        return data


class Coupon_bank(BaseModel):
    """
    我的优惠券
    """
    class Meta:
        verbose_name = "我的优惠券"
        verbose_name_plural = "我的优惠券"
        ordering = ["-create_time",]

    user = models.ForeignKey("Wechat_user",verbose_name="用户",related_name="bank_user")
    descp = models.CharField(max_length = 128,verbose_name="描述",null=True,blank=True)
    share_user = models.ForeignKey("Wechat_user",verbose_name="分享者",related_name="bank_share_user",null=True,blank=True)
    timestamp = models.CharField(max_length=12,verbose_name="时间戳",null=True,blank=True)
    coupon = models.ForeignKey("coupon.Coupon",verbose_name="优惠券",related_name="bank_coupon")
    dead_line = models.DateTimeField(blank=True,null=True,verbose_name="优惠截止日期")

#    def __str__(self):
#        return self.descp
 

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data



class Notice(BaseModel):
    """
    系统通知
    """
    class Meta:
        verbose_name = "系统通知"
        verbose_name_plural = "系统通知"
        ordering = ['-create_time']

    user = models.ForeignKey('Wechat_user',verbose_name="用户",related_name="notice_user")
    text = models.CharField(max_length = 1024,verbose_name = "通知内容")
    is_read = models.BooleanField(verbose_name = "是否已读",default = False)
    
    def __str__(self):
        return self.text

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data



