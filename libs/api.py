# -*- coding: utf-8 -*-
"""
    EauDouce.libs.api
    ~~~~~~~~~~~~~~

    Interface class.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import requests, sys, json
 
from torndb import IntegrityError
from utils.tools import logger,ListEqualSplit,get_today
 
from .base import ServiceBase

class BlogApiManager(ServiceBase ):
 
    def get_source_html(self):
        sql  = "SELECT id,title,content FROM blog_article"
        return self.mysql_read.query(sql)

     
    def blog_get_catalog_data(self, catalog, sort="desc", limit=None):
        "查询分类目录数据"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,catalog,author,create_time FROM blog_article WHERE catalog='%s' ORDER BY id %s %s" %(catalog, sort, LIMIT)
        logger.api.info("query catalog data SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="Catalog data query fail", code=100009)
        else:
            res.update(data=data)

        logger.api.debug(res)
        return res

    def blog_get_sources_data(self, sources, sort="desc", limit=None):
        "查询原创、转载、翻译文章"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        if sources:
            if sources == "1":
                sources = '原创'
            elif sources == "2":
                sources = '转载'
            elif sources == "3":
                sources = '翻译'
            #Original reproduced translation

            sql = "SELECT id,title,sources,author,create_time FROM blog_article WHERE sources='%s' ORDER BY id %s %s" %(sources, sort, LIMIT)
            logger.api.info("query sources data SQL: {}".format(sql))
            try:
                data = self.mysql_read.query(sql)
            except Exception,e:
                logger.api.error(e, exc_info=True)
                res.update(msg="Sources data query fail", code=100001)
            else:
                res.update(data=data)

        logger.api.debug(res)
        return res

    def blog_get_tag_data(self, tag, sort="desc"):
        "查询某个tag的文章"

        res = {"msg": None, "data": [], "code": 0}
        sql = "SELECT id,title,tag,author,create_time FROM blog_article ORDER BY id {}".format(sort)
        logger.api.info("query tag data SQL: {}".format(sql))
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="Tag data query fail", code=100004)
        else:
            tagData = []
            for _ in data:
                #if get_tags_data.decode('utf-8') in _.get('tag').split():
                if tag in _.get('tag').split():
                    tagData.append(_)
            res.update(data=tagData)

        logger.api.debug(res)
        return res


    def blog_get_update_data(self, sort="desc", limit=None):
        "查询更新过的文章"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""      
        sql   = "SELECT id,title,create_time,update_time,tag FROM blog_article WHERE update_time IS NOT NULL ORDER BY update_time %s %s" %(sort, LIMIT)
        logger.api.info("query update_time data SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="query update data fail", code=100007)
        else:
            res.update(data=data)

        logger.api.debug(res)
        return res

    def blog_get_top_data(self, sort="desc", limit=None):
        "查询置顶文章"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,top FROM blog_article ORDER BY update_time %s %s" %(sort, LIMIT)
        logger.api.info("query top data SQL: {}".format(sql))
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="Top data query fail", code=100003)
        else:
            res.update(data=[ _ for _ in data if _.get("top") in ("true", "True", True) ])

        logger.api.debug(res)
        return res

    def blog_get_recommend_data(self, sort="desc", limit=None):
        "查询推荐文章"
        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,recommend FROM blog_article ORDER BY update_time %s %s" %(sort, LIMIT)
        logger.api.info("query recommend data SQL: {}".format(sql))
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="Recommend data query fail", code=100002)
        else:
            res.update(data=[ _ for _ in data if _.get("recommend") in ("true", "True", True) ])

        logger.api.debug(res)
        return res


    def blog_get_catalog_list(self):
        "获取分类目录列表"

        res = {"msg": None, "data": [], "code": 0}
        sql = 'SELECT catalog FROM blog_catalog'
        logger.api.info("query catalog list SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
            data = list(set([ v for _ in data for v in _.values() if v ]))
            #data = [ v.split(",")[0] for i in data for v in i.values() if v and v.split(",")[0] ]
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="query catalog data fail", code=100008)
        else:
            res.update(data=data)

        logger.api.debug(res)
        return res

    def blog_get_tags_list(self):
        "查询所有tag列表"

        res   = {"msg": None, "data": [], "code": 0}
        sql   = "SELECT tag FROM blog_article"
        logger.api.info("query tag list SQL: "+ sql)

        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="Tag list query fail", code=100005)
        else:
            tags = []
            for _ in data:
                if _.get('tag'):
                    tags += _.get("tag").split()
            data = list(set(tags))
            res.update(data=data)

        logger.api.debug(res)
        return res


    def blog_get_single_index(self, sort="desc", limit=None, page=0, length=5):
        "获取所有文章简单数据索引"

        res   = {"msg": None, "data": [], "code": 0, "page": {}}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,tag,author,catalog FROM blog_article ORDER BY id %s %s" %(sort, LIMIT)
        logger.api.info("query single index SQL: %s" %sql)
        try:
            page = int(page)
            blog = self.mysql_read.query(sql)
            data = ListEqualSplit(blog, length)
            length = int(length)
            res.update(statistics=len(blog))
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="query single index fail", code=100006)
        else:
            if page < len(data):
                res.update(data=data[page], page={"page": page, "limit": limit, "length": length, "PageCount": len(data)})
            else:
                logger.api.info("get single index, but IndexOut with page {}".format(page))

        logger.api.debug(res)
        return res

    def blog_get_user_blog(self, user, sort="desc", limit=None):
        "查询某用户的博客 user=uid"

        res   = {"msg": None, "data": [], "code": 0}
        LIMIT = "LIMIT " + str(limit) if limit else ""
        sql   = "SELECT id,title,create_time,update_time,tag,catalog,sources,author from blog_article WHERE author='%s' ORDER BY id %s %s" %(user, sort, LIMIT)
        logger.api.info("query user blog SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update( msg="User blog data query fail", code=1000010)
        else:
            res.update(data=data)
        
        logger.api.debug(res)
        return res

    def blog_refresh_id_cache(self, blogId):
        """刷新某个id博客数据缓存"""
        key = "EauDouce:blog:{}:cache".format(blogId)
        kid = self.redis.delete(key)
        return True if isinstance(kid, (int, long)) else False

    def blog_get_id(self, blogId):
        "查询某个id的博客数据"

        res = {"msg": None, "data": [], "code": 0}
        key = "EauDouce:blog:{}:cache".format(blogId)
        if self.redis.exists(key):
            data = json.loads(self.redis.get(key))
            res.update(data=data)
            logger.api.info("hit blog cache")
        else:
            sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author,recommend,top FROM blog_article WHERE id=%s" %blogId
            try:
                data = self.mysql_read.get(sql)
            except Exception,e:
                logger.api.error(e, exc_info=True)
                res.update(msg="get blog error", code=1000011)
            else:
                res.update(data=data)
                self.redis.set(key, json.dumps(data))
                self.redis.expire(key, 600)

        logger.api.debug(res)
        return res

    def blog_get_all(self, limit=None, sort="desc"):
        "查询所有文章"

        res = {"msg": None, "data": [], "code": 0}
        sql = "SELECT id,title,content,create_time,update_time,tag,catalog,sources,author,recommend,top FROM blog_article ORDER BY id %s %s" %(sort, "LIMIT %s" %limit if limit else "")
        logger.api.info("query all blog SQL: %s" %sql)
        try:
            data = self.mysql_read.query(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="get all blog error", code=1000012)
        else:
            res.update(data=data)

        logger.api.debug(res)
        return res


    def blog_create(self, **kwargs):
        "创建博客文章接口"

        res          = {"msg": None, "success": False, "code": 0}
        blog_title   = kwargs.get('title')
        blog_content = kwargs.get('content')
        blog_tag     = kwargs.get("tag")
        blog_catalog = kwargs.get("catalog", "未分类")
        blog_sources = kwargs.get("sources", "原创")
        blog_author  = kwargs.get("author", "admin")
        blog_ctime   = get_today()

        if blog_title and blog_content and blog_ctime and blog_author:
            sql = 'INSERT INTO blog_article (title,content,create_time,tag,catalog,sources,author) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            logger.api.info(sql %(blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources, blog_author))
            try:
                blog_id  = self.mysql_write.insert(sql, blog_title, blog_content, blog_ctime, blog_tag, blog_catalog, blog_sources, blog_author)
            except Exception,e:
                logger.api.error(e, exc_info=True)
                res.update(msg="Blog article failed to write, please try to resubmit.", code=1000013)
            else:
                res.update(msg="blog write success.", success=True, data=blog_id)
        else:
            res.update(msg="data in wrong format.", code=1000014)

         
        return res

    def blog_update(self, **kwargs):
        "更新博客文章接口"

        res          = {"msg": None, "success": False, "code": 0}
        blog_title   = kwargs.get('title')
        blog_content = kwargs.get('content')
        blog_tag     = kwargs.get("tag")
        blog_catalog = kwargs.get("catalog", "未分类")
        blog_sources = kwargs.get("sources", "原创")
        blog_author  = kwargs.get("author", "admin")
        blog_blogId  = kwargs.get("blogId")
        blog_utime   = get_today()

        try:
            blog_blogId = int(blog_blogId)
        except ValueError,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="blogId form error.", code=1000015)
        else:
            if blog_title and blog_content and blog_utime and blog_author:
                sql = "UPDATE blog_article SET title=%s,content=%s,update_time=%s,tag=%s,catalog=%s,sources=%s,author=%s WHERE id=%s"
                try:
                    self.mysql_write.update(sql, blog_title, blog_content, blog_utime, blog_tag, blog_catalog, blog_sources, blog_author, blog_blogId)
                except Exception,e:
                    logger.api.error(e, exc_info=True)
                    res.update(msg="blog update error.", code=1000016)
                else:
                    res.update(success=True, msg=self.blog_refresh_id_cache(blog_blogId))
            else:
                res.update(msg="blog form error.", code=1000017)

        logger.api.debug(res)
        return res

    def blog_delete(self, blogId):
        "删除文章"

        res = {"msg": None, "success": False, "code": 0}
        sql = "DELETE FROM blog_article WHERE id={}".format(blogId)
        logger.api.info("delete blog sql: "+sql)
        try:
            data = self.mysql_write.execute(sql)
        except Exception,e:
            logger.api.error(e, exc_info=True)
            res.update(msg="delete blog error", code=1000018)
        else:
            res.update(success=True, msg=self.blog_refresh_id_cache(blogId))

        logger.api.debug(res)
        return res

    def blog_get_statistics(self):
        "统计数据查询"
        data = {
            "ArticleTotal": self.blog_get_single_index().get("statistics"),
            "CatalogTotal": len(self.blog_get_catalog_list().get("data")),
            "TagTotal": len(self.blog_get_tags_list().get("data")),
            "CommentTotal": None,
        }
        logger.api.info(data)
        return data
 
class ApiManager(BlogApiManager ):
    pass
