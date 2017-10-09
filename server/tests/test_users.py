import datetime
import json

from server import db
from server import http_response as http_response
from server.models import User
from server.tests.base import BaseTestCase
from server.tests.utils import add_user, EMAIL, PASSWORD, JOHN, JOHN_EMAIL, JOHN_PASSWORD, JANE, JANE_EMAIL, \
    JANE_PASSWORD


class TestUserService(BaseTestCase):
    def _add_user_and_login(self, as_admin):
        user = add_user()
        if as_admin:
            user = User.query.filter_by(email=EMAIL).first()
            user.admin = True
            db.session.commit()
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps(dict(
                email=EMAIL,
                password=PASSWORD
            )),
            content_type='application/json'
        )
        return user, resp_login

    def _add_user_john(self, token, with_password=True):
        john = dict(
            username=JOHN,
            email=JOHN_EMAIL
        )
        if with_password:
            john['password'] = JOHN_PASSWORD

        return self.client.post(
            '/users',
            data=json.dumps(john),
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + json.loads(token)['auth_token'])
        )

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            user, resp_login = self._add_user_and_login(as_admin=True)
            response = self._add_user_john(resp_login.data.decode())
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, http_response.CREATED)
            self.assertIn(f'{JOHN_EMAIL} was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user(JOHN, JOHN_EMAIL, JOHN_PASSWORD)
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, http_response.OK)
            self.assertTrue('created_at' in data['data'])
            self.assertIn(JOHN, data['data']['username'])
            self.assertIn(JOHN_EMAIL, data['data']['email'])
            self.assertIn('success', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        created = datetime.datetime.utcnow() + datetime.timedelta(-30)
        add_user(JOHN, JOHN_EMAIL, JOHN_PASSWORD, created)
        add_user(JANE, JANE_EMAIL, JANE_PASSWORD)
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, http_response.OK)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn(JOHN, data['data']['users'][0]['username'])
            self.assertIn(JOHN_EMAIL, data['data']['users'][0]['email'])
            self.assertIn(JANE, data['data']['users'][1]['username'])
            self.assertIn(JANE_EMAIL, data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json_keys_no_password(self):
        """Ensure error is thrown if the JSON object does not have a password key."""
        with self.client:
            user, resp_login = self._add_user_and_login(as_admin=True)
            response = self._add_user_john(resp_login.data.decode(), with_password=False)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, http_response.BAD_REQUEST)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_not_admin(self):
        with self.client:
            user, resp_login = self._add_user_and_login(as_admin=False)
            response = self._add_user_john(resp_login.data.decode())
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'You do not have permission to do that.')
            self.assertEqual(response.status_code, http_response.UNAUTHORIZED)
