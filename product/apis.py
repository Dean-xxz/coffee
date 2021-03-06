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
            'page_size': ('o', 20),
        }

    def access_db(self, kwarg):
        Product_list = Product.objects.filter(is_active=True,is_terminal=True)
        data = [o.get_json() for o in Product_list]
        for i in data:
            item_ids = i['items']
            i['item_info'] = []
            for j in item_ids:
                item_detail = Item.objects.get(pk = j)
                item_detail = item_detail.get_json()
                item_detail.pop('update_time')
                item_detail.pop('create_time')
                item_detail.pop('is_active')
                category_id = item_detail['category']
                category = Category.objects.get(pk = category_id)
                item_detail['category'] = category.title
                i['item_info'].append(item_detail)
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
            i.pop('items')

        data = dict_pagination_response(data, self.request, int(kwarg['page']), int(kwarg['page_size']))
        return data

    def format_data(self, data):
        return ok_json(data = data)


list_product_api = ProductListAPI().wrap_func()

#后台商品条目列表

class ItemListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'page': ('o', 1),
            'page_size': ('o', 20),
        }

    def access_db(self, kwarg):
        item_list = Item.objects.filter(is_active=True)
        data = [o.get_json() for o in item_list]
        for i in data:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')

        data = dict_pagination_response(data, self.request, int(kwarg['page']), int(kwarg['page_size']))
        return data

    def format_data(self, data):
        return ok_json(data = data)


list_item_api = ItemListAPI().wrap_func()
