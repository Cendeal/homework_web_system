from .token import *
from app.mail import send_email
from app.api_1_0 import api
from flask import request, jsonify, current_app
from app.models import Students
from app import db


# 登陆普通
@api.route('/login', methods=['POST'])
def login():
    jdata = {'code': -1, 'token': ''}
    id = request.values.get('id', '')
    password = request.values.get('password', '')
    user = Students.query.filter_by(id=id).first()
    if user is not None and user.verify_password(password):
        jdata['code'] = 0
        jdata['token'] = user.generate_confirm_token(expiration=3600 * 48).decode('utf-8')
    return jsonify(jdata)


# 注册普通
@api.route('/register', methods=['POST'])
def register():
    id = request.values.get('id', '')
    name = request.values.get('name', '')
    email = request.values.get('email', '')
    password = request.values.get('password', '')
    check_id = Students.query.filter_by(id=id).first()
    jdata = {'code': -1, 'token': ''}
    if check_id is None and name is not '' and email is not '' and len(password) >= 8:
        user = Students()
        user.id = id
        user.name = name
        user.email = email
        user.password = password
        db.session.add(user)
        db.session.commit()
        jdata['code'] = 0
    return jsonify(jdata)


# 修改个人信息
@api.route('/change_profile', methods=['POST'])
def change_profile():
    jdata = {'code': -1, 'token': ''}
    if check_is_login():
        id = request.values.get('id', '')
        name = request.values.get('name', '')
        email = request.values.get('email', '')
        user = Students.query.filter_by(id=id).first()
        change = False
        if name is not '':
            user.name = name
            change = True
        if email is not '':
            user.email = email
            change = True
        if change:
            db.session.add(user)
            db.session.commit()
    jdata['code'] = 0
    return jsonify(jdata)


# 修改密码
@api.route('/change_password', methods=['POST'])
def change_password():
    jdata = {'code': -1, 'data': {}}
    id = request.values.get('id', '')
    old = request.values.get('old', '')
    new = request.values.get('new', '')
    user = Students.query.filter_by(id=id).first()
    if user is not None:
        if user.verify_password(old):
            user.password = new
            jdata['code'] = 0
    return jsonify(jdata)


# 申请学委
@api.route('/apply', methods=['POST'])
def apply():
    jdata = {'code': -1, 'data': {}}
    if check_is_login():
        id = request.values.get('id', '')
        user = Students.query.filter_by(id=id).first()
        jdata['code'] = 0
        send_email(current_app._get_current_object().config['FLASKY_MAIL_SENDER'], '来自' + id + '的申请', '/mail/apply',
                   user=user)
    return jsonify(jdata)
