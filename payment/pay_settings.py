# wechat_pay_settings
WECHAT_PAY_CONFIG = {
    'appid':"wxc59b077d6c26e6ff",
    'mch_id':"1496508102",
    'app_secret':"8050cb55bd7eed9ce2959b3c8f11e3af",
    'key':"sdfasdfsdf13546sdfasdfd555xcfdew",
    'notify_url':"http://www.zhongkakeji.com/payment/notify/"
}


# ali_pay_settings
ALI_PAY_CONFIG = {
    'alipay_key':"yx3m1ogq34j5xywvokgs1oqpgubgqwbk",  # 安全检验码，以数字和字母组成的32位字符
    'alipay_input_charset':"utf-8",
    'alipay_partner':"2088921611153801", # 合作身份者ID，以2088开头的16位纯数字
    'alipay_seller_email':"1330017748@qq.com",  # 签约支付宝账号或卖家支付宝帐户
    'alipay_sign_type':"MD5",
    'alipay_return_url':"",  # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    'alipay_notify_url':"http://www.zhongkakeji.com/payment/notify/",  # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    'alipay_show_url':'',
    'alipay_transport':'http'
}
