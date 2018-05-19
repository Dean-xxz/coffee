from django.db.models import Sum
from machine.models import Channel,Machine
from payment.models import Order

def get_machine_data(mch_id):
    machine_list = Machine.objects.filter(is_active = True,channel_id = mch_id)
    machine_list = [o.get_json() for o in machine_list]
    for machine in machine_list:
        machine_id = machine['id']
        data = Order.objects.filter(is_active = True,is_payment = True,scene = '1',machine_id = machine_id).aggregate(Sum('total_fee'))
        if data['total_fee__sum'] is not None:
            sales_amount = int(data['total_fee__sum'])
        if data['total_fee__sum'] is None:
            sales_amount = 0
        order_count = Order.objects.filter(is_active = True,is_payment = True,scene = '1',machine_id = machine_id).count()
        machine['sales_amount'] = sales_amount
        machine['order_count'] = order_count
        machine['machine_id'] = machine['id']
        machine.pop('create_time')
        machine.pop('update_time')
        machine.pop('is_active')
        machine.pop('id')
        machine.pop('mac_address')
        machine.pop('channel')
        machine.pop('password')
    return machine_list





def get_mch_data():
    mch_list = Channel.objects.filter(is_active = True)
    mch_list = [o.get_json() for o in mch_list]
    for mch in mch_list:
        mch_id = mch['id']
        sales_amount = get_sales_amount(mch_id = mch_id)
        order_count = get_order_count(mch_id = mch_id)
        mch['sales_amount'] = sales_amount
        mch['order_count'] = order_count
        all_amount = Order.objects.filter(is_active = True,is_payment = True,scene = '1').aggregate(Sum('total_fee'))
        all_amount = int(all_amount['total_fee__sum'])
        all_count = Order.objects.filter(is_active = True,is_payment = True,scene = '1').count()
        mch['all_amount'] = all_amount
        mch['all_count'] = all_count
        mch.pop('create_time')
        mch.pop('update_time')
        mch.pop('is_active')
        mch['mch_id'] = mch['id']
        mch.pop('id')
        mch.pop('username')
        mch.pop('password')
    return mch_list

def get_sales_amount(mch_id):
    machine_list = Machine.objects.filter(channel_id = mch_id,is_active = True)
    machine_list = [o.get_json() for o in machine_list]
    sales_amount = 0
    for machine in machine_list:
        machine_id = machine['id']
        mch_order = Order.objects.filter(is_active = True,is_payment = True,scene = '1',machine_id = machine_id).aggregate(Sum('total_fee'))
        sum_data = int(mch_order['total_fee__sum'])
        if sum_data is not None:
            sales_amount = sales_amount + sum_data
        return sales_amount

def get_order_count(mch_id):
    machine_list = Machine.objects.filter(channel_id = mch_id,is_active = True)
    machine_list = [o.get_json() for o in machine_list]
    order_count = 0
    for machine in machine_list:
        machine_id = machine['id']
        count = Order.objects.filter(is_active = True,is_payment = True,scene = '1',machine_id = machine_id).count()
        order_count = order_count + count
    return order_count
