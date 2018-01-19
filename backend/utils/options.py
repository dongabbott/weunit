# -*-coding:utf-8 -*-
# 请求方式配置
REQUEST_METHOD = (
    (1, 'GET'),
    (2, 'POST'),
    (3, 'PUT'),
    (4, 'DELETE')
)

# 项目配配类型
SETTING_CLASS = [
    (0, u"服务地址"),
    (1, u"请求头"),
    (2, u"默认参数"),
    (3, u"数据库"),
    (4, u"登录地址"),
    (5, u"登录默认参数"),
    (6, u"token取值"),
    (7, u"退出登录地址")
]

# 默认请求头
HEADER_DEFAULT = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/vnd.timehut.v5+json",
    "User-Agent": "com.liveyap.timehut/5.1.1.2 (android 7.1.1, OD105) (SOURCE/aliyun, VERSION_CODE/227)"
}