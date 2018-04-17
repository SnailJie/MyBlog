#coding=utf-8
from flask import Blueprint, g, render_template, request, redirect, url_for, make_response, abort

front_blueprint = Blueprint("front", __name__)

@front_blueprint.route("/")
def index():
    return render_template("front/blogIndex.html")


@front_blueprint.route("/bolg/Write")
def blogWrite():
    return render_template("front/blogWrite.html")

@front_blueprint.route("/blog/<int:bid>.html")
def blogShow(bid):
    data = g.api.blog_get_id(bid).get("data")
    if data:
        return render_template("front/blogShow.html", blogId=bid, data=data, original=True if data.get("sources") == "原创" else False)
    else:
        return abort(404)