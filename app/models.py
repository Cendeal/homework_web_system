# 问题如何创建表单 ok
# models的设置
from datetime import datetime

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Permission:
    ADMIN = 16
    WRITE = 8
    NORMAL = 0


class States:
    HIDE = 2
    FINISH = 1
    NOW = 0


# 加载登陆用户
@login_manager.user_loader
def load_user(user_id):
    return Students.query.get(user_id)


# 科目表：科目编号、科目
class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), unique=False)
    houseworks = db.relationship('Houseworks', backref='courses')
    fk_tid = db.Column(db.String(64), db.ForeignKey('teamnumbers.id'))

    def to_json(self):
        json_courses = {
            'id': self.id,
            'name': self.name,
            'tid': self.fk_tid
        }
        return json_courses

    def __repr__(self):
        return '<Courses %r>' % self.name


# 浏览记录表
class ReadHistory(db.Model):
    __tablename__ = 'readhistory'
    readdate = db.Column(db.DateTime, default=datetime.utcnow)
    # 外键
    fk_sid = db.Column(db.String(8), db.ForeignKey('students.id'), primary_key=True)
    fk_hid = db.Column(db.Integer, db.ForeignKey('houseworks.id'), primary_key=True)


# 作业表：创建日期、外键科目编号、标题、内容、状态、外键班别号
class Houseworks(db.Model):
    __tablename__ = 'houseworks'
    createdate = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=False)
    content = db.Column(db.UnicodeText, unique=False)
    state = db.Column(db.Integer, unique=False)
    # 关系属性
    picsave = db.relationship('PicSave', backref='houseworks')
    readhistory = db.relationship('ReadHistory',
                                  foreign_keys=[ReadHistory.fk_hid],
                                  backref=db.backref('readwork', lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all,delete-orphan')
    # 外键班别号
    fk_tid = db.Column(db.String(64), db.ForeignKey('teamnumbers.id'))
    # 外键courses.id
    fk_cid = db.Column(db.String(64), db.ForeignKey('courses.id'))

    def to_json(self):
        json_housework = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'state': self.state,
            'fk_cid': self.fk_cid,
            'fk_tid': self.fk_tid,
            'creatdate': str(self.createdate)
        }
        return json_housework

    def __repr__(self):
        return '<Houseworks %r>' % self.title


# 班别表：班别编号
class Teamnumbers(db.Model):
    __tablename__ = 'teamnumbers'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), default=id)
    tag = db.Column(db.String(8), default=None)

    houseworks = db.relationship('Houseworks', backref='teamnbers')
    courses = db.relationship('Courses', backref='teamnbers')
    emailsender = db.relationship('EmailSender', backref='teamnbers')
    students = db.relationship('Students', backref='teamnbers')

    def is_this_admin(self, student):
        return self.fk_sid == student.get_id()

    def __repr__(self):
        return '<Teamnumbers %r>' % self.id


# 学生表
class Students(UserMixin, db.Model):
    __tablename__ = 'students'
    id = db.Column(db.String(8), primary_key=True)
    perm = db.Column(db.Integer, unique=False, default=Permission.NORMAL)
    password_hash = db.Column(db.String(128), unique=False)
    name = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=False)
    isComfirm = db.Column(db.Boolean, default=False)
    # 外键
    fk_tid = db.Column(db.String(64), db.ForeignKey('teamnumbers.id'))

    # 关系属性
    readhistory = db.relationship('ReadHistory',
                                  foreign_keys=[ReadHistory.fk_sid],
                                  backref=db.backref('readuser', lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all,delete-orphan')
    picsave = db.relationship('PicSave', backref='students')
    emailsender = db.relationship('EmailSender', backref='students')

    @property
    def password(self):
        raise ArithmeticError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirm_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.isComfirm = True
        db.session.add(self)
        return True

    def is_admin(self):
        return self.perm >= Permission.WRITE

    def __repr__(self):
        return '<Students %r>' % self.id

    def to_json(self):
        keys = vars(self).items()
        data = {}
        for k, v in keys:
            if k != '_sa_instance_state' and k != 'password_hash':
                data[k] = v
        return data


# 图片保存表
class PicSave(db.Model):
    __tablename__ = 'picsave'
    path = db.Column(db.String(256), primary_key=True)
    # 外键
    fk_workid = db.Column(db.Integer, db.ForeignKey('houseworks.id'))
    fk_sid = db.Column(db.String(64), db.ForeignKey('students.id'))


# 开通通知表
class EmailSender(db.Model):
    __tablename__ = 'emailsender'
    isopen = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(64))
    fk_sid = db.Column(db.String(8), db.ForeignKey('students.id'), primary_key=True)
    fk_tid = db.Column(db.String(64), db.ForeignKey('teamnumbers.id'), primary_key=True)
