from unittest import TestCase
from app import app
from models import db, connect_db, User
thing = User('Tom', 'Thomson', 'abc')


class appTestCase(TestCase):
  """tests for app.py"""
  userInt = 0

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