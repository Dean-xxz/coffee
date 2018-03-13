#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 支付模块所需公共api
"""

from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

# from .models import
#
# # 广告列表接口
#
#
# class AdListAPI(AbstractAPI):
#     def config_args(self):
#         self.args = {
#         }
#
#     def access_db(self, kwarg):
#         ad_list = Advertisement.objects.filter(is_active=True)
#         data = [o.get_json for o in ad_list]
#
#         return data
#
#     def format_data(self, data):
#         return ok_json(data = data)
#
#
# list_ad_api = AdListAPI().wrap_func()