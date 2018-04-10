import json
from django.db import models
from utils.basemodel.base import BaseModel
from django.core import serializers

# Create your models here.

class Advertisement(BaseModel):

    """
    咖啡机终端app轮播广告
    """
    title = models.CharField(max_length=128,verbose_name="广告标题",null=True,blank=True)
    link = models.CharField(max_length=128,verbose_name="广告链接",null=True,blank=True)
    is_terminal = models.BooleanField(verbose_name="是否终端显示",default=False)
    image = models.ImageField(upload_to="media/ad/img/",verbose_name="广告图片",null=True,blank=True)
    video = models.FileField(upload_to="media/ad/video/",verbose_name="广告视频",null=True,blank=True)
    order = models.PositiveSmallIntegerField(verbose_name = "顺序",default = 1,help_text = "该广告在广告列表中的顺序")
    remarks = models.TextField(verbose_name="备注、描述",null=True,blank=True,help_text="请输入备注、描述等")


    class Meta:
        verbose_name = "轮播广告"
        verbose_name_plural = "轮播广告"
        ordering = ["order",]

    def __str__(self):
        return self.title

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data
