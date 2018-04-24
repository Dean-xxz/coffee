import json
from django.db import models
from utils.basemodel.base import BaseModel
from django.core import serializers
from django.conf import settings
from product.models import Item
from accounts.models import Wechat_user


class Access_Code(BaseModel):

    """
    咖啡机原料容器表
    """
    item = models.ForeignKey("product.Item",verbose_name="商品条目",related_name="code_item")
    user = models.ForeignKey("accounts.Wechat_user", related_name="access_code_user",null=True,blank=True)
    code = models.CharField(max_length=6,verbose_name="提货码")
    status = models.BooleanField(verbose_name="是否使用",default=False)


    class Meta:
        verbose_name = "提货码"
        verbose_name_plural = "提货码"
        ordering = ['-create_time',]


    def __str__(self):
        return self.code

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data
