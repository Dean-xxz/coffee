#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 产品所需公共api
"""

from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI
from utils.paginator import json_pagination_response, dict_pagination_response

from .models import Category,Item,Product

#

# 终端产品列表

class ProductListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'page': ('o', 1),
            'page_size': ('o', 8),
        }

    def access_db(self, kwarg):
        Product_list = Product.objects.filter(is_active=True,is_terminal=True)
        data = [o.get_json() for o in Product_list]
        for i in data:
            item_id = i['items']
            item_detail = Item.objects.get(pk = item_id)
            item_detail = item_detail.get_json()
            category_id = item_detail['category']
            category = Category.objects.get(pk = category_id)
            item_detail['category'] = category.title
            i['item'] = item_detail

        data = dict_pagination_response(data, self.request, int(kwarg['page']), int(kwarg['page_size']))
        return data

    def format_data(self, data):
        return ok_json(data = data)


list_product_api = ProductListAPI().wrap_func()

