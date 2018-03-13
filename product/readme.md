此模块为整个平台产品模块，提供所有销售得产品及产品组合信息

产品分类表：Category
    id：key
    title：char 分类标题

产品内容表: item
    id:key
    category:foreign_key
    info:char 产品内容
    img:图片

一个产品可以包含多个产品内容

产品表：product
    id：key
    title：char 产品标题
    img：产品大图
    image：产品小图
    descp：char 产品描述
    sources：manytomany 商品内容
    price：int 产品价格
    vip_price: int 优惠价格
    count：int  数量
    remark：char 备注
    order：int  排序
