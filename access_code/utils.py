import random
from .models import Access_Code
from product.models import Item

def get_access_code(user_id,item_id):
    code = ''.join(random.sample(['A', 'B', 'C', 'D', 'E', 'F', '1', '2', '3', '4','5','6','7','8','9','0'],6)).replace("", "")
    access_code = Access_Code(item_id = item_id,user_id = user_id,code = code)
    access_code.save()
    return access_code


def get_first_access_code(user_id,item_id):
    code = ''.join(random.sample(['A', 'B', 'C', 'D', 'E', 'F', '1', '2', '3', '4','5','6','7','8','9','0'],6)).replace("", "")
    access_code = Access_Code(item_id = item_id,user_id = user_id,code = code,is_send = False)
    access_code.save()
    return access_code
