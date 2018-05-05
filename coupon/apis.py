#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖商城优惠券模块所需公共api
"""
import json
import datetime

from django.conf import settings
from django.core import serializers
from django.db.models import Q
from urllib.request import urlopen

from utils.paginator import json_pagination_response, dict_pagination_response
from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

from .models import Coupon
from accounts.models import Coupon_bank
from accounts.models import Wechat_user

class CouponbankCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            "user_id":'r',
            "share_user_id":'r',
        }

    def access_db(self, kwarg):
        user_id = kwarg['user_id']
        share_user_id = kwarg['share_user_id']
        
        count = Coupon_bank.objects.filter(share_user_id = share_user_id).count()
        if count > 10:
            return None
        coupon = Coupon.objects.filter().order_by('?')[:1]
        data = [o.get_json() for o in coupon]
        coupon_id = data[0]['id']
        deadline = data[0]['dead_line']
        couponbank = Coupon_bank(share_user_id=share_user_id,user_id=user_id,coupon_id=coupon_id,dead_line=deadline)
        couponbank.save()
        if couponbank:
            data = {}
            share_user = Wechat_user.objects.get(pk=share_user_id)
            data['share_user_info'] = share_user.get_json()
            user = Wechat_user.objects.get(pk=user_id)
            data['user_info'] = user.get_json()
            coupon = Coupon.objects.get(pk=coupon_id)
            data['coupon_info'] = coupon.get_json()
            return data
        return None
    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)
        return fail_json('优惠已被强光')


create_couponbank_api = CouponbankCreateAPI().wrap_func()



class CouponbankListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            "share_user_id":'r',
        }

    def access_db(self, kwarg):
        share_user_id = kwarg['share_user_id']

        coupon = Coupon_bank.objects.filter(share_user_id = share_user_id)
        data = [o.get_json() for o in coupon]
        for i in data:
            share_user_id = i['share_user']
            coupon_id = i['coupon']
            user_id = i['user']
            share_user = Wechat_user.objects.get(pk=share_user_id)
            i['share_user_info'] = share_user.get_json()
            user = Wechat_user.objects.get(pk=user_id)
            i['user_info'] = user.get_json()
            coupon = Coupon.objects.get(pk=coupon_id)
            coupon = coupon.get_json()
            i['coupon_info'] = coupon
            i.pop('is_active')
            i.pop('create_time') 
            i.pop('user')
            i.pop('share_user')
            i.pop('coupon')
            i.pop('descp')
            i.pop('id')
            i.pop('update_time')
        return data

    def format_data(self, data):
        return ok_json(data = data)


list_couponbank_api = CouponbankListAPI().wrap_func()
