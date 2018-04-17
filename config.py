#coding=utf-8
from os import getenv

GLOBAL = {
    "ProcessName": "MyBlog",
    "HOST":"0.0.0.0",
    "Port":"10141"
    }

SSO = {

    "app_name": getenv("eaudouce_sso_app_name", GLOBAL["ProcessName"]),
    # SSO中注册的应用名

    "app_id": getenv("eaudouce_sso_app_id", "app_id"),
    # SSO中注册返回的`app_id`

    "app_secret": getenv("eaudouce_sso_app_secret", "app_secret"),
    # SSO中注册返回的`app_secret`

    "sso_server": getenv("eaudouce_sso_server", "https://passport.saintic.com"),
    # SSO完全合格域名根地址
}

MYSQL=getenv("eaudouce_mysql_url","mysql://localhost:3306:root:onceas:saintic")
#MYSQL数据库连接信息
#mysql://host:port:user:password:database?charset=&timezone=


REDIS=getenv("eaudouce_redis_url","redis://@localhost:6379")
#Redis数据库连接信息，格式：
#redis://[:password]@host:port/db
#host,port必填项,如有密码,记得密码前加冒号,默认localhost:6379/0
