import json
from django.db import models
from utils.basemodel.base import BaseModel
from django.core import serializers


# Create your models here.


class Category(BaseModel):

    """
    产品分类表
    """
    title = models.CharField(max_length=128, verbose_name="产品分类标题")
    descp = models.CharField(max_length=1024,verbose_name="分类描述",null=True,blank=True)
    image = models.ImageField(upload_to="media/product/category/image/",verbose_name="产品分类介绍图片",null=True,blank=True)
    order = models.PositiveSmallIntegerField(verbose_name="排序",default=0,help_text="在列表中的顺序")

    class Meta:
        verbose_name = "产品分类"
        verbose_name_plural = "产品分类"
        ordering = ['order',]

    def __str__(self):
        return self.title

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


class Item(BaseModel):

    """
    商品条目表
    """
    title = models.CharField(max_length=128, verbose_name="条目标题")
    english_title = models.CharField(max_length=128,verbose_name="英文名",null=True,blank=True)
    can_select = models.BooleanField(verbose_name = "是否冷热可选",default = True)
    category = models.ForeignKey("Category",
                                 verbose_name = "所属产品分类",
                                 related_name = "categorys")
    descp = models.CharField(max_length=1024,verbose_name="商品描述",null=True,blank=True)
    image = models.ImageField(upload_to="media/product/item/image/",verbose_name="商品图片",null=True,blank=True)
    order = models.PositiveSmallIntegerField(verbose_name="排序",default=0,help_text="在列表中的顺序")


    class Meta:
        verbose_name = "商品条目"
        verbose_name_plural = "商品条目"
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


# 一款产品可以包含一个或多个产品条目

class Product(BaseModel):

    """
    产品表
    """
    title = models.CharField(max_length=128, verbose_name="产品标题")
    english_title = models.CharField(max_length=128,verbose_name="英文标题",null=True,blank=True)
    descp = models.CharField(max_length=1024,verbose_name="产品描述",null=True,blank=True)
    big_image = models.ImageField(upload_to="media/product/product/image/",verbose_name="产品大图",help_text="尺寸：260px*260px",null=True,blank=True)
    small_image = models.ImageField(upload_to="media/product/product/small_img/",verbose_name="产品小图",help_text="尺寸：162px*162px",null=True,blank=True)
    makret_big_image = models.ImageField(upload_to="media/product/product/market_big_img/",verbose_name="商城产品大图",help_text="尺寸：162px*162px",null=True,blank=True)
    market_small_image = models.ImageField(upload_to="media/product/product/market_small_img/",verbose_name="商城产品小图",help_text="尺寸：162px*162px",null=True,blank=True)
    items = models.ManyToManyField("Item",verbose_name="商品条目",help_text="请选择该商品包含得产品内容")
    price = models.DecimalField(max_digits=10 ,decimal_places =0,verbose_name="产品价格")
    vip_price = models.DecimalField(max_digits=10,decimal_places=0,verbose_name="产品优惠价格")
    count = models.IntegerField(verbose_name="数量",default=1)
    is_terminal = models.BooleanField(verbose_name="是否终端显示",default=True)
    is_suit = models.BooleanField(verbose_name="是否为套餐商品",default=False)
    is_discount = models.BooleanField(verbose_name="是否为打折商品",default=False)
    is_hot = models.BooleanField(verbose_name="是否为热销商品",default=False)
    order = models.PositiveSmallIntegerField(verbose_name="顺序",default=0,help_text="该产品在产品列表中的顺序")
    remarks = models.TextField(verbose_name="备注",null=True,blank=True)


    class Meta:
        verbose_name = "产品表"
        verbose_name_plural = "产品表"
        ordering = ['order',]

    def __str__(self):
        return self.title

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data
