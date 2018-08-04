#此处可以定义一个蓝本，导入视图view,导入model
from flask import Blueprint
main = Blueprint('main',__name__)
#注意顺序
from .import views,errors
