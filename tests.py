from unittest import TestCase
from unittest.mock import MagicMock
import sqlalchemy as sa
from sqlalchemy import MetaData
import contextlib 
from app import app
from models import db, connect_db, User, Post
thing = User('Tom', 'Thomson', 'abc')




# meta = MetaData()
# meta.reflect(bind=engine)
# with contextlib.closing(engine.connect()) as con:
#   trans = con.begin()
#   for table in reversed(meta.sorted_tables):
#     con.execute(table.delete())
#   trans.commit()

# connect_db()



class appTestCase(TestCase):
  """tests for app.py"""
  userInt = 0

  # def empty_database(engine, metadata):
  #   metadata.drop_all(engine)
  #   metadata.create_all(engine)
  
  # engine = sa.create_


  def test_home(self):
    with app.test_client() as client:
      res = client.get('/')
      html = res.get_data(as_text = True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('<h1>Blogly</h1>', html)

  def test_users_list(self):
    with app.test_client() as client:
      res = client.get('/user/list')
      html = res.get_data(as_text = True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('<h1>User list</h1>', html)

  # def test_new_user(self):
  #   with app.test_client() as client:
  #     res = client.get('/user/new')
  #     html = res.get_data(as_text = True)

  #     self.assertEqual(res.status_code, 200)
  #     self.assertIn('<h1>New User</h1>', html)

  #     res = client.post(
  #       '/user/new', data={
  #         'first-name': 'Tom',
  #         'last-name': 'Thomson'})
      
  #     html = res.get_data(as_text = True)

  #     self.assertEqual(res.status_code, 302)
  #     self.assertEqual(res.location, 'http://localhost/user/list')

      # self.assertTrue(db.user.filter(db.user.first_name == 'Tom',
      #                                db.user.last_name == 'Thomson'))
      
      # html = client.get('/user/list')
      # html = res.get_data(as_text = True)
      # self.assertIn(f'<a href="/user/{self.userInt}">Tom Thomson</a>', html)


  # def test_user_details(self):
  #   with app.test_client() as client:
  #     res = client.get(f'/user/{self.userInt}')
  #     html = res.get_data(as_text = True)