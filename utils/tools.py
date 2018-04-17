#coding=utf-8
from log import Logger
import re, hashlib, datetime, random,  time, hmac

class DO(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

logger          = DO(
                    sys = Logger("sys").getLogger,
                    api = Logger("api").getLogger,
                    err = Logger("error").getLogger,
                    access = Logger("access").getLogger,
                    plugin = Logger("plugin").getLogger
                  )
get_today       = lambda format="%Y-%m-%d %H:%M":datetime.datetime.now().strftime(format)

ListEqualSplit  = lambda l,n=5: [ l[i:i+n] for i in range(0,len(l), n) ]

def ParseMySQL(mysql, callback="dict"):
    """解析MYSQL配置段"""
    if not mysql:return None
    protocol, dburl = mysql.split("://")
    if "?" in mysql:
        dbinfo, dbargs  = dburl.split("?")
    else:
        dbinfo, dbargs  = dburl, "charset=utf8&timezone=+8:00"
    host,port,user,password,database = dbinfo.split(":")
    charset, timezone = dbargs.split("&")[0].split("charset=")[-1] or "utf8", dbargs.split("&")[-1].split("timezone=")[-1] or "+8:00"
    if callback in ("list", "tuple"):
        return protocol,host,port,user,password,database,charset, timezone
    else:
        return {"Protocol": protocol, "Host": host, "Port": port, "Database": database, "User": user, "Password": password, "Charset": charset, "Timezone": timezone}
