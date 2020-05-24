# coding:utf-8
import json
import os
import hashlib
import re
from datetime import datetime
from flask import flash, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc
from app import db, mail
from app.mail import send_email
from app.main.form import LoginForm, RegistrationForm, EditProfileForm, ChangePassword, WorkForm, WorkFormEidt, \
    CourseForm
from . import main
from ..models import Courses, Houseworks, Students, States, Teamnumbers, Permission, ReadHistory, PicSave, EmailSender


@main.route("/homework/addCourses", methods=['POST', 'GET'])
@login_required
def addCourses():
    if current_user.is_admin():
        form = CourseForm()
        if form.validate_on_submit():
            tid = current_user.fk_tid
            course = Courses(id=form.id.data,
                             name=form.name.data,
                             fk_tid=tid)
            db.session.add(course)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash('更新数据失败！')
            return redirect(url_for('main.info'))
        return render_template('/addcourses.html', form=form)
    else:
        return render_template('/404.html')


@main.route("/homework/addWork", methods=['POST', 'GET'])
@login_required
def addWork():
    if current_user.is_admin():
        form = WorkForm()
        tid = current_user.fk_tid
        form.courses.choices = [(c.id, c.name) for c in Courses.query.filter_by(fk_tid=tid).order_by('name')]
        if form.validate_on_submit():
            housework = Houseworks(fk_tid=tid, title=form.title.data,
                                   state=int(form.state.data),
                                   content=form.content.data,
                                   createdate=datetime.now(),
                                   fk_cid=form.courses.data)
            content = housework.content
            patten = re.compile("<img[^>]*>")
            src = patten.findall(content)
            print(src)
            srcnew = [i.replace(' ', '').replace('<imgsrc="', 'app').replace('"style="max-width:100%;">', '') for i in
                      src]
            db.session.add(housework)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash('更新数据失败！')
            for i in srcnew:
                pic = PicSave.query.filter_by(path=i, fk_sid=current_user.id).first()
                if pic is not None:
                    pic.fk_workid = housework.id
                    print(housework.id)
                    db.session.add(pic)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                        flash('更新数据失败！')
            delpic = PicSave.query.filter_by(fk_sid=current_user.id, fk_workid=None).all()
            for p in delpic:
                os.remove(p.path)
                db.session.delete(p)
                db.session.commit()
            cname = Courses.query.filter_by(id=housework.fk_cid).first().name
            sendto = EmailSender.query.filter_by(fk_tid=tid, isopen=True).all()
            print(sendto)

            for i in sendto:
                user = Students.query.filter_by(id=i.fk_sid).first()
                send_email(i.email, '来自' + i.fk_tid + '的' + cname + '(有新消息)', '/mail/mail', info=housework,user=user)
            return redirect(url_for('main.info'))
        return render_template('/addwork.html', form=form)
    else:
        return render_template('/404.html')


@main.route('/homework/changePassword', methods=['POST', 'GET'])
@login_required
def changePassword():
    form = ChangePassword()
    if form.validate_on_submit():
        user = Students.query.filter_by(id=current_user.id).first()
        if user.verify_password(form.ordinalPassword.data):
            user.password = form.password.data
            db.session.add(user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash('更新数据失败！')
            flash("修改成功")
        else:
            flash("原密码不匹配")
            return render_template('/changePassword.html', form=form)
        return redirect(url_for('main.profile'))
    return render_template('/changePassword.html', form=form)


@main.route('/homework/changeProfile', methods=['POST', 'GET'])
@login_required
def changeProfile():
    form = EditProfileForm()

    if form.validate_on_submit():
        user = Students.query.filter_by(id=current_user.id).first()
        if user.name == form.name.data and user.email == form.email.data:
            flash('个人信息没有发生改变')
        else:
            if user.name != form.name.data:
                user.name = form.name.data
            if user.email != form.email.data:
                user.email = form.email.data
                user.isComfirm = False
                emailsender = EmailSender.query.filter_by(fk_sid=user.id,fk_tid=user.fk_tid).first()
                emailsender.email=user.email
                db.session.add(emailsender)
            db.session.add(user)

            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash('更新数据失败！')
        return redirect(url_for('main.profile'))
    form.name.data = current_user.name
    form.email.data = current_user.email
    return render_template('/changeProfile.html', form=form)


@main.route('/homework/changegroupid', methods=['GET'])
@login_required
def changegroupid():
    if current_user.perm == Permission.ADMIN:
        id = request.args['id']
        groupid = request.args['newgroup']
        if len(groupid) != 6:
            flash('群组长度不对，请确认为六位！')
            return 'fail'
        user = Students.query.filter_by(id=id).first()
        print(user.fk_tid)
        if user is not None and user.fk_tid != groupid:
            user.fk_tid = groupid
            db.session.add(user)
            try:
                db.session.commit()
            except:
                db.rollback()
            flash('修改成功！')
            return 'ok'
        else:
            flash('修改失败(groupid)')
            return 'fail'


# 修改权限
@main.route('/homework/changeState', methods=['GET'])
@login_required
def changerState():
    if current_user.perm == Permission.ADMIN:
        id = request.values.get('id')
        perm = request.values.get('perm')
        if current_user.id != id:
            user = Students.query.filter_by(id=id).first()
            user.perm = int(perm)
            db.session.add(user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash('更新数据失败！')
            flash('修改权限成功!')
        else:
            flash('修改失败!')
    return redirect(url_for('main.manageuser'))


@main.route('/homework/confirmemail')
@login_required
def confirmemail():
    token = request.args['token']
    comfirm = current_user.confirm(token.encode())
    if comfirm:
        flash('验证成功！')
    else:
        flash('验证失败！')
    return redirect(url_for('main.profile'))


@main.route('/homework/deletecourses/<id>')
@login_required
def deletecourses(id):
    if current_user.is_admin():
        tid = current_user.fk_tid
        course = Courses.query.filter_by(id=id, fk_tid=tid).first()
        rmWorks = Houseworks.query.filter_by(fk_cid=id).all()
        if course is not None:
            db.session.delete(course)
            for i in rmWorks:
                picsave = PicSave.query.filter_by(fk_workid=i.id, fk_sid=current_user.id).all()
                for p in picsave:
                    os.remove(p.path)
                    db.session.delete(p)
                readhistory = ReadHistory.query.filter_by(fk_hid=i.id).all()
                for c in readhistory:
                    db.session.delete(c)
                db.session.delete(i)
            db.session.commit()
            flash('删除成功！')
        else:
            flash('操作失败！')
        return redirect(url_for('main.manage'))
    else:
        return render_template('/404.html'), 404


@main.route('/homework/delete/<id>')
@login_required
def deleteid(id):
    if current_user.is_admin():
        work = Houseworks.query.filter_by(id=int(id)).first()
        readhistory = ReadHistory.query.filter_by(fk_hid=int(id)).all()
        picsave = PicSave.query.filter_by(fk_workid=int(id), fk_sid=current_user.id).all()
        if work is not None:
            for p in picsave:
                os.remove(p.path)
                db.session.delete(p)
            for i in readhistory:
                db.session.delete(i)
            db.session.delete(work)
            db.session.commit()
            flash('删除成功！')
        else:
            flash('操作失败！')
        return redirect(url_for('main.manage'))
    else:
        return render_template('/404.html'), 404


# 删除用户
@main.route('/homework/deleteuser/<id>')
@login_required
def deleteiduser(id):
    if current_user.perm == Permission.ADMIN:
        user = Students.query.filter_by(id=id).first()
        emailsender = EmailSender.query.filter_by(fk_sid=id).all()
        readhistory = ReadHistory.query.filter_by(fk_hid=int(id)).all()
        if user is not None and current_user.id != id:
            for e in emailsender:
                db.session.delete(e)
            for r in readhistory:
                db.session.delete(r)
            db.session.delete(user)
            db.session.commit()
            flash('删除成功！')
        else:
            flash('操作失败！')
        return redirect(url_for('main.manageuser'))
    elif current_user.perm == 8:
        user = Students.query.filter_by(id=id).first()
        if user is not None and current_user.id != id and user.perm < current_user.perm and current_user.fk_tid == user.fk_tid:
            db.session.delete(user)
            db.session.commit()
            flash('删除成功！')
        else:
            flash('操作失败！')
        return redirect(url_for('main.manageuser'))
    else:
        return render_template('/404.html'), 404


@main.route('/homework/generatetoken')
@login_required
def generatetoken():
    token = current_user.generate_confirm_token().decode('utf-8')

    send_email(current_user.email, '确认你的邮箱!', '/mail/comfirm', token=token)
    flash('验证邮件已经发送到你的邮箱,请查看！')
    return redirect(url_for('main.profile'))


def get_dict_hosework(current_user, is_manage = False):
    num = current_user.fk_tid
    courses = Courses.query.filter_by(fk_tid=num).all()
    dict_for_course = []
    for i in courses:
        if is_manage is not True:
            hasread = Houseworks.query.join(ReadHistory,
                                            ReadHistory.fk_hid == Houseworks.id).filter(
                Houseworks.fk_tid == num,
                Houseworks.fk_cid == i.id,
                ReadHistory.fk_sid == current_user.id,
                Houseworks.state != States.HIDE
            ).all()
        else:
            hasread = Houseworks.query.join(ReadHistory,
                                            ReadHistory.fk_hid == Houseworks.id).filter(
                Houseworks.fk_tid == num,
                Houseworks.fk_cid == i.id,
                ReadHistory.fk_sid == current_user.id
            ).all()
        if is_manage:
            hide = len(Houseworks.query.filter_by(fk_tid=num, fk_cid=i.id).all())
        else:
            hide = len(Houseworks.query.filter_by(fk_tid=num, fk_cid=i.id,state=States.HIDE).all())
        temp = {'id': i.id,
                'list': Houseworks.query.filter(Houseworks.fk_tid == num,
                                                Houseworks.fk_cid == i.id,
                                                Houseworks.state != States.HIDE).order_by(
                    desc(Houseworks.createdate)).all(),
                'hide': hide,
                'name': i.name,
                'read': [hasread, len(hasread)],
                'len': 0}
        temp['len'] = len(temp['list'])
        dict_for_course.append(temp)
    return dict_for_course, num


@main.route('/homework/')
def index():
    return render_template('/main.html')


@main.route('/homework/info')
@login_required
def info():
    dict_for_course, num = get_dict_hosework(current_user)

    return render_template('/info.html', dict_for_course=dict_for_course, num=num)


@main.route('/homework/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Students.query.filter_by(id=form.id.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效密码或账号！')
    return render_template('/login.html', form=form)


@main.route('/homework/logout')
@login_required
def logout():
    logout_user()
    flash('已登出')
    return redirect(url_for('main.login'))


@main.route("/homework/manage")
@login_required
def manage():
    if current_user.is_admin():
        dict_for_course, num = get_dict_hosework(current_user)
        return render_template('/manage.html', dict_for_course=dict_for_course, num=num)
    else:
        return render_template('/404.html')


@main.route("/homework/manage/<id>", methods=['POST', 'GET'])
@login_required
def manageid(id):
    if current_user.is_admin():
        work = Houseworks.query.filter_by(id=int(id)).first()
        form = WorkFormEidt()
        if form.validate_on_submit():
            patten = re.compile("<img[^>]*>")
            oldpiccontent = work.content
            work.title = form.title.data
            work.content = form.content.data
            work.state = int(form.state.data)
            db.session.add(work)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash('更新数据失败！')
            content = work.content

            src = patten.findall(content)
            oldsrc = patten.findall(oldpiccontent)
            srcnew = [i.replace(' ', '').replace('<imgsrc="', 'app').replace('"style="max-width:100%;">', '') for i in
                      src]
            srcold = [i.replace(' ', '').replace('<imgsrc="', 'app').replace('"style="max-width:100%;">', '') for i in
                      oldsrc]
            for i in srcnew:
                if i not in srcold:
                    pic = PicSave.query.filter_by(path=i, fk_sid=current_user.id).first()
                    if pic is not None:
                        if pic.fk_workid is None:
                            pic.fk_workid = work.id
                            db.session.add(pic)
                            try:
                                db.session.commit()
                            except:
                                db.session.rollback()
                                flash('更新数据失败！')
            for i in srcold:
                if i not in srcnew:
                    delpic = PicSave.query.filter_by(path=i).first()
                    os.remove(delpic.path)
                    db.session.delete(delpic)
                    db.session.commit()
            delpic = PicSave.query.filter_by(fk_sid=current_user.id, fk_workid=None).all()
            for p in delpic:
                os.remove(p.path)
                db.session.delete(p)
                db.session.commit()
            return redirect(url_for('main.manage'))
        form.title.data = work.title
        form.state.data = str(work.state)
        content = work.content.replace('\r', '').replace('\n', '<br>').replace('\t', '&nbsp;&nbsp;')
        content = '<p>' + content + '</p>'
        return render_template('/editwork.html', form=form, content=content)
    else:
        return render_template('/404.html'), 404


@main.route('/homework/manageuser')
@login_required
def manageuser():
    if current_user.perm == 16:
        userlist = Students.query.order_by(Students.id).all()
        userbelong = Students.query.filter_by(fk_tid=None).all()

        for i in userbelong:
            i.fk_tid = i.id[:6]
            db.session.add(i)
            try:
                db.session.commit()
            except:
                db.session.rollback()
        return render_template('/manageuser.html', userlist=userlist, id=None)
    elif current_user.perm == 8:
        userlist = Students.query.filter_by(fk_tid=current_user.fk_tid).order_by(Students.id).all()
        return render_template('/managegroup.html', userlist=userlist,id=None)
    else:
        return render_template('/404.html'), 404


@main.route('/homework/openemail')
@login_required
def openemail():
    sid = current_user.id
    print(sid)
    isopen = False
    if request.args['isopen'] == 'True':
        isopen = True
    else:
        isopen = False
    print(request.args['isopen'],isopen)
    stu = Students.query.filter_by(id=sid).first()
    if stu.isComfirm:
        emailsender = EmailSender.query.filter_by(fk_sid=sid, fk_tid=current_user.fk_tid).first()
        print(emailsender)
        if emailsender is None:
            emailsender = EmailSender(email=current_user.email, fk_sid=sid, isopen=isopen, fk_tid=current_user.fk_tid)
        else:
            emailsender.isopen = isopen
        db.session.add(emailsender)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('更新数据失败！')
    else:
        flash('请先到【个人信息】验证邮箱！')
    return redirect(url_for('main.profile'))


@main.route('/homework/profile')
@login_required
def profile():
    cid = current_user.fk_tid

    emailsender = EmailSender.query.filter_by(email=current_user.email,fk_sid=current_user.id).first()
    if emailsender is None:
        emailsender = EmailSender(email=current_user.email, fk_sid=current_user.id, fk_tid=cid)
        db.session.add(emailsender)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('更新数据失败(1)！')
    return render_template('profile.html', user=current_user, cid=cid, emailsender=emailsender)


@main.route('/homework/read')
@login_required
def read():
    infoid = request.args['infoid']
    isread = request.args['isread']
    info = Houseworks.query.filter_by(id=infoid, fk_tid=current_user.fk_tid).first()

    if info is not None:
        if isread == 'False' and ReadHistory.query.filter_by(fk_sid=current_user.id, fk_hid=info.id).first() is None:
            whoreading = ReadHistory(readdate=datetime.now(), fk_sid=current_user.id, fk_hid=info.id)
            print(whoreading.fk_sid, whoreading.readdate, whoreading.fk_hid)
            db.session.add(whoreading)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash('更新数据失败！')
        members = ReadHistory.query.filter_by(fk_hid=info.id).all()
        count = len(members)
        return render_template('detail.html', info=info, count=count, members=members)
    else:
        return render_template('/404.html')


@main.route('/homework/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if len(form.id.data) == 8:
            tid = form.id.data[0:len(form.id.data) - 2]
            t = Teamnumbers.query.filter_by(id=tid).first()
            if t is None:
                t = Teamnumbers(id=tid)
                db.session.add(t)
                db.session.commit()
            user = Students(email=form.email.data,
                            id=form.id.data,
                            name=form.name.data,
                            fk_tid=form.id.data[:6],
                            password=form.password.data)
            db.session.add(user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash('更新数据失败！')

            flash('你可以登陆了！')
        else:
            return '404'
        return redirect(url_for('main.login'))
    return render_template('/register.html', form=form)


@main.route('/homework/search', methods=['GET'])
@login_required
def search():
    id = request.args['id']
    if id == '':
        return redirect(url_for('main.manageuser'))
    user = None
    if current_user.perm == Permission.WRITE:
        user =Students.query.filter_by(id=id,fk_tid=current_user.fk_tid).first()
    elif current_user.perm == Permission.ADMIN:
        user=Students.query.filter_by(id=id).first()
    else:
        return render_template('/404.html'), 404
    if user is None:
        return render_template('/manageuser.html', userlist=None, id=id)
    else:
        ls = []
        ls.append(user)
        return render_template('/manageuser.html', userlist=ls, id=id)


@main.route('/homework/upload', methods=['POST'])
@login_required
def upload():
    data = []
    for i in request.files:
        t = request.files[i]
        name = hashlib.md5((i + current_user.id + str(datetime.now())).encode('utf-8')).hexdigest()
        sufix = i[i.rfind('.'):len(i)]
        path = 'app/static/upload/' + name + sufix
        t.save(path)
        data.append(url_for('static', filename='upload/' + name + sufix))
        picsave = PicSave(fk_sid=current_user.id, path=path)
        db.session.add(picsave)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('更新数据失败！')
        json_data = {"errno": 0, "data": data}
    return json.dumps(json_data)
