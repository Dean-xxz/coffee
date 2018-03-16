#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技app 配方模块所需公共api
"""

from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

from .models import Formula,Container
from product.models import Item

# 配方查询接口

class FormulaQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'item_id':'r',
        }

    def access_db(self, kwarg):
        item_id = kwarg['item_id']

        formula = Formula.objects.filter(item_id=item_id,is_active=True)
        data = [o.get_json() for o in formula]
        for i in data:
            container_id = i['container']
            container = Container.objects.get(pk=container_id)
            container_name = container.title
            item = Item.objects.get(pk=item_id)
            item_title = item.title
            i['item_title'] = item_title
            i['container_name'] = container_name
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
            i.pop('remarks')
            i.pop('id')
        return data

    def format_data(self, data):
        return ok_json(data = data)


query_formula_api = FormulaQueryAPI().wrap_func()
