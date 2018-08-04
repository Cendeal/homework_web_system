# 获取作业信息
from .. import db
from ..models import Houseworks, Courses
from . import api
import json


@api.route('/task/<id>')
def get_task_tid(id):
    houseworklist = Houseworks.query.filter_by(fk_tid=id).order_by(Houseworks.fk_cid).all()
    json_list = []
    for i in houseworklist:
        json_list.append(i.to_json())
    return json.dumps(json_list)


@api.route('/courses')
def get_courses():
    clist = Courses.query.all()
    json_list = []

    for i in clist:
        json_list.append(i.to_json())
    return json_list
