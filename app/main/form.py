from flask_login import current_user
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, RadioField
from wtforms.validators import Length, DataRequired, Email, EqualTo, Regexp, ValidationError

# 登陆表格
from app.models import Students, Courses


class LoginForm(Form):
    id = StringField('学号', validators=[Length(8), DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('登陆')


# 注册表格
class RegistrationForm(Form):
    id = StringField('学号*(长度为8)', validators=[DataRequired(),
                                       Length(8, 8),
                                       Regexp('^[0-9]*$', 8, '学号为数字')])
    name = StringField('姓名*', validators=[DataRequired(),
                                         Length(2, 64)])
    email = StringField('邮箱*', validators=[DataRequired(),
                                          Length(1, 64),
                                          Email()])
    password = PasswordField('密码*(长度范围4-24)', validators=[DataRequired(),
                                                         Length(4, 24),
                                                         EqualTo('password2', message='两次输入不匹配，请重新输入！')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')


    def validate_id(self, field):
        if Students.query.filter_by(id=field.data).first():
            raise ValidationError('学号已存在！')


# 修改信息
class EditProfileForm(Form):
    name = StringField('姓名', validators=[DataRequired(),
                                         Length(2, 64)])
    email = StringField('邮箱', validators=[DataRequired(),
                                          Length(1, 64),
                                          Email()])
    submit = SubmitField('确定修改')


# 添加作业
# 作业表：创建日期、外键科目编号、标题、内容、状态、外键班别号
class WorkForm(Form):
    courses = SelectField('科目', validators=[DataRequired()])
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    content = TextAreaField('内容',validators=[DataRequired()])
    state = RadioField(label='状态', choices=[('1', '已结束'), ('0', '进行ing')], default='0')
    submit = SubmitField('提交')

# 修改作业
class WorkFormEidt(Form):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    content = TextAreaField(label='内容',validators=[DataRequired()])
    state = RadioField(label='状态', choices=[('1', '已结束'), ('0', '进行ing'),('2','隐藏')], default='0')
    submit = SubmitField('提交')


# 修改密码
class ChangePassword(Form):
    ordinalPassword = PasswordField('原来密码', validators=[DataRequired()])
    password = PasswordField('新密码*(长度范围4-24)', validators=[DataRequired(),
                                                          Length(4, 24),
                                                          EqualTo('password2', message='两次输入不匹配，请重新输入！')])
    password2 = PasswordField('再次确定密码', validators=[DataRequired()])
    submit = SubmitField('确定修改')


# 添加科目
class CourseForm(Form):

    id = StringField('科目编号(填数字少于64位)', validators=[DataRequired(), Length(0, 64)])
    name = StringField('科目名称', validators=[DataRequired(), Length(0, 64)])
    submit = SubmitField('提交')

    def validate_id(self, field):
        if Courses.query.filter_by(id=field.data).first():
            raise ValidationError('编号已存在！')
    def validate_name(self,field):
        curTeamId =current_user.id[0:len(current_user.id) - 2]
        curCourse=Courses.query.filter_by(name=field.data).first()
        if  curCourse!=None and curCourse.fk_tid == curTeamId:
            raise ValidationError('科目已存在！')

