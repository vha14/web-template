from sqlalchemy.exc import IntegrityError

from server import db
from server.models import User
from server.tests.base import BaseTestCase
from server.tests.utils import add_user, NAME, EMAIL, PASSWORD
from server.auth import encode_auth_token, decode_auth_token


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user()
        self.assertTrue(user.id)
        self.assertEqual(user.username, NAME)
        self.assertEqual(user.email, EMAIL)
        self.assertTrue(user.password)
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)
        self.assertFalse(user.admin)

    def test_user_to_json(self):
        user_json = add_user().to_json()
        self.assertEqual(user_json['username'], NAME)
        self.assertEqual(user_json['email'], EMAIL)
        self.assertTrue('id' in user_json)
        self.assertTrue('created_at' in user_json)
        self.assertTrue('admin' in user_json)
        self.assertTrue('active' in user_json)
        self.assertFalse('password' in user_json)

    def test_add_user_duplicate_username(self):
        add_user()
        duplicate_user = User(
            username=NAME,
            email='test@test2.com',
            password=PASSWORD
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user()
        duplicate_user = User(
            username='justanothertest',
            email=EMAIL,
            password=PASSWORD
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_decode_auth_token(self):
        user = add_user()
        auth_token = encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(decode_auth_token(auth_token), user.id)
