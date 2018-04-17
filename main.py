#coding=utf-8
import time, os.path, jinja2, sys, rq_dashboard
from flask import Flask, request, g, render_template, redirect, make_response, url_for
from config import GLOBAL
from view.front import front_blueprint
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

#注册blue print 
app.register_blueprint(front_blueprint)


@app.route('/')
def index():
    return redirect(url_for("front.index"))

if __name__ == '__main__':
    app.run(host=GLOBAL.get('HOST'), port=int(GLOBAL.get('Port')), debug=True)