#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供众咖科技商户平台 销售模块所需公共api
"""
import json
from django.db.models import Q
from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI
from .models import Order
from machine.models import Machine,Machine_state,Material_state
from product.models import Product,Item,Category
from .crm_utils import get_mch_data,get_machine_data
from formula.models import Container

#商户平台销售数据筛选接口
class SaleListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'product_id':('o',None),
            'time':('o',None),
        }

    def access_db(self, kwarg):
        product_id = kwarg['product_id']
        time = kwarg['time']
        if product_id is None and time is None:
            data = get_mch_data()
            return data
        if product_id is None and time is not None:
            data = get_mch_time_data(time = time)
            return data
        if product_id is not None and time is None:
            data = get_mch_product_data(product_id = product_id)
            return data
        if product_id is not None and time is not None:
            data = get_mch_detail_data(product_id = product_id,time = time)
            return data

    def format_data(self, data):
        return ok_json(data = data)

list_sale_api = SaleListAPI().wrap_func()

#单个商户每台机器销售数据列表接口
class MachineSaleListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'mch_id':'r',
            'product_id':('o',None),
            'time':('o',None),
        }

    def access_db(self, kwarg):
        product_id = kwarg['product_id']
        time = kwarg['time']
        mch_id = kwarg['mch_id']

        if product_id is None and time is None:
            data = get_machine_data(mch_id = mch_id)
            return data
#        if product_id is None and time is not None:
#            data = get_mch_time_data(time = time)
#            return data
#        if product_id is not None and time is None:
#            data = get_mch_product_data(product_id = product_id)
#            return data
#        if product_id is not None and time is not None:
#            data = get_mch_detail_data(product_id = product_id,time = time)
#            return data


    def format_data(self, data):
        return ok_json(data = data)

list_machine_sale_api = MachineSaleListAPI().wrap_func()


#机器列表接口
class MachineListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'mch_id':'r',
        }

    def access_db(self, kwarg):
        mch_id = kwarg['mch_id']
        
        machine_list = Machine.objects.filter(channel_id = mch_id,is_active = True)
        machine_list = [o.get_json() for o in machine_list]
        for machine in machine_list:
            machine['machine_id'] = machine['id']
            machine.pop('id')
            machine.pop('create_time')
            machine.pop('update_time')
            machine.pop('is_active')
            machine.pop('password')
            return machine_list

    def format_data(self, data):
        return ok_json(data = data)

list_machine_api = MachineListAPI().wrap_func()

#机器列表统计接口
class MachineCountAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'mch_id':'r',
        }

    def access_db(self, kwarg):
        mch_id = kwarg['mch_id']

        error_count = Machine.objects.filter(channel_id = mch_id,is_active = True,error_state = '2').count()
        networking_count = Machine.objects.filter(channel_id = mch_id,is_active = True,is_networking = False).count()
        material_count = Machine.objects.filter(channel_id = mch_id,is_active = True,material_state = '3').count()
        machine_count = Machine.objects.filter(channel_id = mch_id,is_active = True).count()
        data = {
            'machine_count':machine_count,
            'error_count':error_count,
            'material_count':material_count,
            'networking_count':networking_count,
        }
        return data

    def format_data(self, data):
        return ok_json(data = data)

count_machine_api = MachineCountAPI().wrap_func()


#缺料机器列表接口
class MachineMaterialListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'mch_id':'r',
        }

    def access_db(self, kwarg):
        mch_id = kwarg['mch_id']

        machine_list = Machine.objects.filter(channel_id = mch_id,is_active = True).filter(Q(material_state = '2')|Q(material_state = '3'))
        machine_list = [o.get_json() for o in machine_list]
        for machine in machine_list:
            machine_id = machine['id']
            material_state = Material_state.objects.filter(machine_id = machine_id)
            material_state = [o.get_json() for o in material_state]
            for i in material_state:
                container_id = i['container']
                container = Container.objects.get(pk = container_id)
                container_name = container.title
                i['container_name'] = container_name
                i.pop('create_time')
                i.pop('update_time')
                i.pop('is_active')
                i.pop('container')
            machine['material_detail'] = material_state
            machine['machine_id'] = machine['id']
            machine.pop('id')
            machine.pop('create_time')
            machine.pop('update_time')
            machine.pop('is_active')
            machine.pop('password')
            return machine_list

    def format_data(self, data):
        return ok_json(data = data)

list_machinematerial_api = MachineMaterialListAPI().wrap_func()

#缺料详情查询接口
class MaterialQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'machine_id':'r',
        }

    def access_db(self, kwarg):
        machine_id = kwarg['machine_id']
        
        detail = Material_state.objects.filter(machine_id = machine_id)
        data = [o.get_json() for o in detail]
        return data

    def format_data(self, data):
        return ok_json(data = data)

query_material_api = MaterialQueryAPI().wrap_func()


#故障机器列表
class MachineErrorListAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'mch_id':'r',
        }

    def access_db(self, kwarg):
        mch_id = kwarg['mch_id']

        machine_list = Machine.objects.filter(channel_id = mch_id,is_active = True,error_state = '2')
        machine_list = [o.get_json() for o in machine_list]
        for machine in machine_list:
            machine_id = machine['id']
            error_detail = Machine_state.objects.filter(machine_id = machine_id,is_cannel = False)
            error_detail = [o.get_json() for o in error_detail]
            for error in error_detail:
                error.pop('update_time')
                error.pop('is_active')
            machine['error_detail'] = error_detail
            machine['machine_id'] = machine['id']
            machine.pop('id')
            machine.pop('create_time')
            machine.pop('update_time')
            machine.pop('is_active')
            machine.pop('password')
            return machine_list

    def format_data(self, data):
        return ok_json(data = data)

list_machineerror_api = MachineErrorListAPI().wrap_func()


#故障详情查询接口
class ErrorQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'machine_id':'r',
        }

    def access_db(self, kwarg):
        machine_id = kwarg['machine_id']

        detail = Error_state.objects.filter(machine_id = machine_id,is_cannel = False)
        data = [o.get_json() for o in detail]
        return data

    def format_data(self, data):
        return ok_json(data = data)

query_error_api = ErrorQueryAPI().wrap_func()
