import unittest

from flask import url_for
from flask_testing import TestCase

from application import app, db, bcrypt
from application.models import Users, Transactions, OutgoingTransaction
from os import getenv


class TestBase(TestCase):
  def create_app(self):

      # pass in configurations for test database
    config_name = 'testing'
    app.config.update(TEST_DATABASE_URI=getenv('mysql+pymysql://root:root@35.246.125.7/testdb'),
                      TEST_SECRET_KEY=getenv('smtb98'),
                      WTF_CSRF_ENABLED=False,
                      DEBUG=True
                      )
    return app

  def setUp(self):
    db.session.commit()
    db.drop_all()
    db.create_all()

    hashed_test_pw = bcrypt.generate_password_hash('Testing123Testing')
    userData = Users(
        first_name="Forename",
        last_name="Surname",
        email="test@testemail.co.uk",
        password=hashed_test_pw
    )
    db.session.add(userData)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()


class TestViews(TestBase):
  def test_homepage_view(self):
    response = self.client.get(url_for('home'))
    self.assertEqual(response.status_code, 200)

  def test_register_view(self):
    response = self.client.get(url_for('register'))
    self.assertEqual(response.status_code, 200)
  
  def test_login_view(self):
    response = self.client.get(url_for('login'))
    self.assertEqual(response.status_code, 200)

  def test_add_outgoing_transaction(self):
    with self.client:
      self.client.post(
          url_for('login'),
          data=dict(
            email='test@testemail.co.uk',
            password='Testing123Testing'
          ),
          follow_redirects=True
      )
      response = self.client.get(url_for('outgoing_transaction'))
      self.assertEqual(response.status_code, 200)

  def test_add_incoming_transaction(self):
    with self.client:
      self.client.post(
          url_for('login'),
          data=dict(
            email='test@testemail.co.uk',
            password='Testing123Testing'
          ),
          follow_redirects=True
      )
      response = self.client.get(url_for('incoming_transaction'))
      self.assertEqual(response.status_code, 200)
  
  def test_account(self):
    with self.client:
      self.client.post(
          url_for('login'),
          data=dict(
            email='test@testemail.co.uk',
            password='Testing123Testing'
          ),
          follow_redirects=True
      )
      response = self.client.get(url_for('account'))
      self.assertEqual(response.status_code, 200)
  
  def test_new_transaction(self):
    with self.client:
      self.client.post(
          url_for('login'),
          data=dict(
            email='test@testemail.co.uk',
            password='Testing123Testing'
          ),
          follow_redirects=True
      )
      response = self.client.get(url_for('new_transaction'))
      self.assertEqual(response.status_code, 200)