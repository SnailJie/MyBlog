from flask import Blueprint, g, render_template, request, redirect, url_for, make_response, abort

front_blueprint = Blueprint("front", __name__)

@front_blueprint.route("/")
def index():
    return render_template("front/blogIndex.html")