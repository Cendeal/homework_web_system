from app import getApp, db
from flask_script import Manager, Shell

app = getApp('production')
manage = Manager(app)


@manage.command
def initApp():
    db.create_all()


if __name__ == '__main__':
    manage.run()
