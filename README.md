
#### 简介
```
主要用于班级作业通知与管理的网站
```
#### 功能
- 1.普通成员：
```
1）浏览学习委员发布的作业通知
2）认证邮箱，是否开启邮箱通知
```
- 2.学委
```
1）可以编辑、修改、删除和发布作业通知等相关作业的操作；
2）管理成员：可以通过id的查找、可以删除本班成员
4）可上传图片，插入在线媒体标签，比如音乐、视频等
```
- 3.高级管理员
```
1)可以管理所有成员
2)可以修改普通成员的所属班别
另外，系统默认为开启邮箱通知的用户发送邮件
```
#### 开发用到的技术：
```
1.部署系统是Ubuntu,采用的是gunicorn Wsgi Http Server,[链接](http://gunicorn.org/，同时应用了nginx反向代理)
2.作业编辑器采用了开源的富文本wangEditor,[链接](http://www.wangeditor.com)
3.前端框架使用的bootstrap v3,因为需求css有一点小改动
4.Web应用框架使用的是Flask
5.数据库Mysql 5.5.6
```
#### 技术要点：
1.认证用户
> 用户登录之后，记录用户认证状态，实现用户多个页面切换依然记住用户的认证状态

- 方案使用Flask-Login

[1].安装扩展
```
pip install flask-login
```

[2].用户模型`app/model.py`
```
from flask_login import UserMixin
...
class Students(UserMixin, db.Model):
    __tablename__ = 'students'
...
```
[3].初始化LoginManager:`app/ __init__.py`
```
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
def getApp(config_name):
 ...
    login_manager.init_app(app)
 ...
```
[4].回调函数的实现：`app/model.py`
```
from . import login_manager
...
@login_manager.user_loader
def load_user(user_id):
    return Students.query.get(user_id)
...
```
2.富文本wangEditor的使用
> 需求 
（1）把原来的内容文本框换成富文本wangEditor
（2）实现图片的实时上传

- 需求（1）方案：隐藏原来文本输入框，构建新的wangEditor，当按下'提交'时，把内容赋值到被隐藏的文本输入框
`templates/editwork.html`
```

...

 <script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/wangEditor.min.js') }}"></script>
    <script type="text/javascript">

        var $text1 = $('#content')
        $text1.hide()
        $text1.after('<div id=\'editor\' class=\'form-group\'></div>')
        $ed = $('#editor')
        var E = window.wangEditor
        var editor = new E('#editor')
        editor.customConfig.menus = [
            'head',  // 标题
            'bold',  // 粗体
            'fontSize',  // 字号
            'fontName',  // 字体
            'italic',  // 斜体
            'underline',  // 下划线
            'strikeThrough',  // 删除线
            'foreColor',  // 文字颜色
            'backColor',  // 背景颜色
            'link',  // 插入链接
            'list',  // 列表
            'justify',  // 对齐方式
            'quote',  // 引用
            'emoticon',  // 表情
            'image',  // 插入图片
            'video',  // 插入视频
            'code',  // 插入代码
            'undo',  // 撤销
            'redo'  // 重复
        ]
        $ed.html('{{ content|safe }}')
        editor.customConfig.uploadImgServer = '/homework/upload'
        editor.customConfig.uploadImgMaxSize = 3 * 1024 * 1024
        editor.create()
        // 初始化 textarea 的值
        document.getElementById('submit').addEventListener('click', function () {
            $text1.val(editor.txt.html())
        }, false)
    </script>

...

```
- 需求（2）方案：对上传的临时图片进行保存，上传的图片的名字进行了md5处理后会在数据库进行保存,当用户提交了之后这条数据会被增加一个指向的houseworkid的值，并且会对没有hfk_workid的图片进行清理。
`app/main/view.py`
```

...

# 保存图片
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

...

# 图片处理代码片段,从数据库中找出没有fk_workid的进行删除
    delpic = PicSave.query.filter_by(fk_sid=current_user.id,fk_workid=None).all()
    for p in delpic:
                os.remove(p.path)
                db.session.delete(p)
                db.session.commit()

...


```

#### 演示
![演示.gif](https://upload-images.jianshu.io/upload_images/4413333-db5cf797d9c015f3.gif?imageMogr2/auto-orient/strip)

![管理用户1](https://upload-images.jianshu.io/upload_images/4413333-8e6ab7d8d01a0edb.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![管理用户2](https://upload-images.jianshu.io/upload_images/4413333-8e5e99601573d1be.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![管理用户3](https://upload-images.jianshu.io/upload_images/4413333-0c31a1de607b04d8.PNG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




#### 源码
[homework_web_system](https://github.com/Cendeal/homework_web_system)
#### 预览地址
http://www.cendeal.cn/homework




