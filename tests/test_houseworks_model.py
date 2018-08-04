import unittest
from datetime import datetime
from app import getApp, db
from app.models import Houseworks, Permission, States, Teamnumbers, Courses, Students


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = getApp('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_hosework(self):
        s = Students(id='04160909', perm=Permission.WRITE)
        t = Teamnumbers(id='041609', fk_sid=s.id)
        c = Courses(id='01', name='英语')
        c2 = Courses(id='02', name='数学')
        c3 = Courses(id='03', name='语文')
        h = Houseworks(createdate=datetime.now(),
                       title='英语作业1',
                       content='完成单元1测试',
                       fk_cid=c.id, fk_tid=t.id,
                       state=States.NOW)
        h3 = Houseworks(createdate=datetime.now(),
                        title='语文作业1',
                        content='完成单元1测试',
                        fk_cid=c3.id, fk_tid=t.id,
                        state=States.NOW)
        h4 = Houseworks(createdate=datetime.now(),
                        title='数学作业1',
                        content='完成单元1测试',
                        fk_cid=c2.id, fk_tid=t.id,
                        state=States.NOW)
        h5 = Houseworks(createdate=datetime.now(),
                        title='数学作业2',
                        content='完成单元1测试',
                        fk_cid=c2.id, fk_tid=t.id,
                        state=States.NOW)
        h6 = Houseworks(createdate=datetime.now(),
                        title='数学作业3',
                        content='完成单元1测试',
                        fk_cid=c2.id, fk_tid=t.id,
                        state=States.NOW)
        h7 = Houseworks(createdate=datetime.now(),
                        title='英语作业2',
                        content='完成单元2测试',
                        fk_cid=c.id, fk_tid=t.id,
                        state=States.NOW)
        s2 = Students(id='04160809', perm=Permission.ADMIN)
        t2 = Teamnumbers(id='041608', fk_sid=s2.id)
        h2 = Houseworks(createdate=datetime.now(),
                        title='英语作业1',
                        content='完成单元1测试',
                        fk_cid=c.id, fk_tid=t2.id,
                        state=States.NOW)
        db.session.add_all([s, t, c, h, s2, t2, h2, c2, c3, h3, h4, h5, h6, h7])
        db.session.commit()
        self.assertEqual(h.fk_tid, t.id)
        print(h.to_json())
