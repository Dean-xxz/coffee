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
            'item_id':('o',None),
        }

    def access_db(self, kwarg):
        item_id = kwarg['item_id']

        if item_id:
            formula = Formula.objects.filter(item_id=item_id,is_active=True).order_by('order')
            data = [o.get_json() for o in formula]
            for i in data:
                container_id = i['container']
                container = Container.objects.get(pk=container_id)
                container_name = container.title
                container_id = container.order
                i['container_id'] = container_id
                item = Item.objects.get(pk=item_id)
                i['hotcoolchoice'] = item.can_select
                item_title = item.title
                i['item_title'] = item_title
                i['container_name'] = container_name
                print (type(i['effluentinterval']))
                i['effluentinterval'] = float(i['effluentinterval'])
                i.pop('create_time')
                i.pop('update_time')
                i.pop('is_active')
                i.pop('remarks')
                i.pop('id')
            return data
        item_list = Item.objects.filter(is_active=True)
        data = [o.get_json() for o in item_list]
        for i in data:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
            i.pop('category')
            item_id = i['id']
            formula = Formula.objects.filter(item_id=item_id,is_active=True).order_by('order')
            formula_list = [o.get_json() for o in formula]
            item_title = i['title']
            hotcoolchoice = i['can_select']
            for j in formula_list:
                container_id = j['container']
                container = Container.objects.get(pk=container_id)
                container_name = container.title
                container_id = container.order
                j['item_title'] = item_title
                j['hotcoolchoice'] = hotcoolchoice
                j['container_id'] = container_id
                j['container_name'] = container_name
                j['effluentinterval'] = float(j['effluentinterval'])
                j.pop('create_time')
                j.pop('update_time')
                j.pop('is_active')
                j.pop('remarks')
                j.pop('id')
            i['formula_detail'] = formula_list
        return data

    def format_data(self, data):
        return ok_json(data = data)


query_formula_api = FormulaQueryAPI().wrap_func()

#料盒列表接口
class ContainerListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
        }

    def access_db(self, kwarg):
        container = Container.objects.filter(is_active=True)
        data = [o.get_json() for o in container]
        for i in data:
            i.pop('create_time')
            i.pop('update_time')
            i.pop('is_active')
        return data

    def format_data(self, data):
        return ok_json(data = data)


list_container_api = ContainerListAPI().wrap_func()
