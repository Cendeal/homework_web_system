# 获取作业信息
from ..models import Houseworks, Courses, ReadHistory
from . import api
from flask import jsonify
from .token import *


# 获取个人信息
@api.route('/profile')
def profile():
    jdata = {'code': -1, 'data': {}}
    if check_is_login():
        id = request.values.get('id')
        user = Students.query.filter_by(id=id).first()
        jdata['data'] = user.to_json()
        jdata['code'] = 0
    return jsonify(jdata)


# 获取某一次具体的作业
@api.route('/work_detail/<hid>')
def get_work_detail(hid):
    jdata = {'code': -1, 'data': {}}
    if check_is_login():
        work = Houseworks.query.filter_by(id=hid).first()
        if work is not None:
            jdata['data'] = work.to_json()
            jdata['data']['read_count'] = work.readhistory.count()
            jdata['code'] = 0
    return jsonify(jdata)


# 获取某一科所有作业列表
@api.route('/task/<cid>')
def get_task_tid(cid):
    jdata = {'code': -1, 'data': {}}
    if check_is_login():
        result = Courses.query.filter_by(id=cid).first()

        json_list = []
        if result is not None:
            houseworklist = result.houseworks
            for i in houseworklist:
                reads = i.readhistory.count()
                print(reads)
                data = {'read_count': reads, 'title': i.title, 'hid': i.id}
                json_list.append(data)
        jdata['data']['list'] = json_list
        jdata['code'] = 0
    return jsonify(jdata)


# 获取某一班级的所有作业科目列表
@api.route('/courses/<tid>')
def get_courses(tid):
    jdata = {'code': -1, 'data': {}}
    if check_is_login():

        clist = Courses.query.filter_by(fk_tid=tid).all()
        json_list = []
        for i in clist:
            json_list.append(i.to_json())
        jdata['data']['list'] = json_list
        jdata['code'] = 0
    return jsonify(jdata)


# 获取某一次作业的具体阅读记录
@api.route('/read_history/<hid>')
def read_history(hid):
    jdata = {'code': -1, 'data': {}}
    if check_is_login():
        dt = []
        r = ReadHistory.query.filter_by(fk_hid=hid).all()
        if r is not None:
            for i in r:
                data = {'xh': i.fk_sid, 'time': i.readdate}
                dt.append(data)
        jdata['data']['list'] = dt
        jdata['code'] = 0
    return jsonify(jdata)
