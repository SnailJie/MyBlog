# -*- coding: utf-8 -*-
"""
    EauDouce.views.api
    ~~~~~~~~~~~~~~

    Foreground interface view.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import time
from torndb import IntegrityError
from flask import request, g, Blueprint, abort
from flask_restful import Api, Resource
from libs.api import BlogApiManager
from utils.tools import logger
class Blog(Resource):

    def get(self):
        """
        1.limit(int), 限制列出数据数量，默认None，全局参数。
        2.sort(str), 数据排序, desc、asc，默认desc，全局参数。
        3.blogId(int), 查询某一个id的文章, 独立参数。
        4.get_catalog_list(bool), 列出博客所有目录，独立参数。
        5.get_tags_list(bool),
        6.get_catalog_data(str), 查询博客某目录下的limit个文章。
        7.get_sources_data(str), 查询博客某来源下的limit个文章，1是原创，2是转载，3是翻译。
        8.get_index(bool),仅仅查询所有博客标题、ID、创建时间。
        9.get_user(str),查询某用户的所有博客。
        10.get_update_data(bool)，查询更新过的文章
        11.get_top_data(bool)，查询置顶文章
        12.get_recommend_data(bool)，查询推荐文章
        13.get_tags_data(str)，查询某标签下的文章
        14.q(str), 查询标题
        15.get_all_blog(bool), 查询所有文章
        """
        limit  = request.args.get('limit', None)
        sort   = request.args.get('sort', 'desc')
        blogId = request.args.get('blogId', None)
        q      = request.args.get('q')

        get_catalog_data  = request.args.get("get_catalog_data")
        get_sources_data  = request.args.get("get_sources_data")
        get_tags_data     = request.args.get("get_tags_data")

        get_update_data   = True if request.args.get("get_update_data") in ("true", "True", True) else False
        get_top_data      = True if request.args.get("get_top_data") in ("true", "True", True) else False
        get_recommend_data= True if request.args.get("get_recommend_data") in ("true", "True", True) else False

        get_tags_list    = True if request.args.get("get_tags_list") in ("true", "True", True) else False
        get_catalog_list = True if request.args.get("get_catalog_list") in ("true", "True", True) else False

        get_user  = request.args.get("get_user")
        get_index = True if request.args.get("get_index") in ("true", "True", True) else False
        get_all_blog = True if request.args.get("get_all_blog") in ("true", "True", True) else False
        get_banner = True if request.args.get("get_banner") in ("true", "True", True) else False

        if get_banner:
            return g.api.get_banner()

        if request.args.get("get_source_html") in ("true", "True", True):
            return g.api.get_source_html()

        if blogId:
            return g.api.blog_get_id(blogId)

        if get_catalog_data:
            return g.api.blog_get_catalog_data(get_catalog_data, sort, limit)
        if get_sources_data:
            return g.api.blog_get_sources_data(get_sources_data, sort, limit)
        if get_tags_data:
            return g.api.blog_get_tag_data(get_tags_data, sort)

        if get_update_data:
            return g.api.blog_get_update_data(sort, limit)
        if get_top_data:
            return g.api.blog_get_top_data(sort, limit)
        if get_recommend_data:
            return g.api.blog_get_recommend_data(sort, limit)

        if get_tags_list:
            return g.api.blog_get_tags_list()
        if get_catalog_list:
            return g.api.blog_get_catalog_list()

        if get_user:
            return g.api.blog_get_user_blog(get_user, sort, limit)
        if get_index:
            page   = int(request.args.get("page", 0))
            length = int(request.args.get("length", 5))
            return g.api.blog_get_single_index(sort, limit, page, length)
        if get_all_blog:
            return g.api.blog_get_all()

        if q:
            return g.api.blog_search(q)

    def post(self):
        """ 创建博客文章接口 """
        
        data = dict(
            title   = request.form.get('title'),
            content = request.form.get('content'),
            tag     = request.form.get("tag"),
            catalog = request.form.get("catalog", "未分类"),
            sources = request.form.get("sources", "原创"),
            author  = request.form.get("author", "admin")
        )
        logger.sys.debug(data)
        return g.api.blog_create(**data)

    def put(self):
        """ 更新博客文章接口 """
        data = dict(
            title   = request.form.get('title'),
            content = request.form.get('content'),
            tag     = request.form.get("tag"),
            catalog = request.form.get("catalog", "未分类"),
            sources = request.form.get("sources", "原创"),
            author  = request.form.get("author", "admin"),
            blogId  = request.form.get("blogId")
        )
        logger.sys.debug(data)
        return g.api.blog_update(**data)
        
    def delete(self):
        """ 删除博客文章接口 """
        blogId = request.args.get("blogId")
        return g.api.blog_delete(blogId)
       
 

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)
api.add_resource(Blog, '/blog', '/blog/', endpoint='blog')

