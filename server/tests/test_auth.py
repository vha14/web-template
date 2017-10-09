import json

import time

from server import db
from server.models import User
from server.tests.base import BaseTestCase
from server.tests.utils import add_user, TEST_USER, NAME, EMAIL, PASSWORD, JOHN, JOHN_EMAIL, JOHN_PASSWORD
from server import http_response as http_response


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(TEST_USER),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, http_response.CREATED)

    def test_user_registration_duplicate_email(self):
        add_user()
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username=JOHN,
                    email=EMAIL,
                    password='test'
                )),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, http_response.BAD_REQUEST)
            data = json.loads(response.data.decode())
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_duplicate_username(self):
        add_user()
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username=NAME,
                    email='test@test.com2',
                    password='test'
                )),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, http_response.BAD_REQUEST)
            data = json.loads(response.data.decode())
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, http_response.BAD_REQUEST)
            data = json.loads(response.data.decode())
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, http_response.BAD_REQUEST)
            data = json.loads(response.data.decode())
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(username='justatest', password='test')),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, http_response.BAD_REQUEST)
            data = json.loads(response.data.decode())
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(username='justatest', email='test@test.com')),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, http_response.BAD_REQUEST)
            data = json.loads(response.data.decode())
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_valid_logout(self):
        add_user()
        with self.client:
            # user login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type='application/json'
            )
            # valid token logout
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            self.assertEqual(response.status_code, http_response.OK)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')

    def test_invalid_logout_expired_token(self):
        add_user()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type='application/json'
            )
            # invalid token logout
            time.sleep(4)
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            self.assertEqual(response.status_code, http_response.UNAUTHORIZED)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'ExpiredSignatureError')

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers=dict(Authorization='Bearer invalid'))
            self.assertEqual(response.status_code, http_response.UNAUTHORIZED)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'DecodeError')

    def test_user_status(self):
        add_user()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            self.assertEqual(response.status_code, http_response.OK)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == NAME)
            self.assertTrue(data['data']['email'] == EMAIL)
            self.assertTrue(data['data']['active'] is True)
            self.assertTrue(data['data']['created_at'])

    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers=dict(Authorization='Bearer invalid'))
            self.assertEqual(response.status_code, http_response.UNAUTHORIZED)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'DecodeError')

    def test_invalid_logout_inactive(self):
        add_user()
        # update user
        user = User.query.filter_by(email=EMAIL).first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            self.assertEqual(response.status_code, http_response.UNAUTHORIZED)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Something went wrong. Please contact us.')

    def test_invalid_status_inactive(self):
        add_user()
        # update user
        user = User.query.filter_by(email=EMAIL).first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            self.assertEqual(response.status_code, http_response.UNAUTHORIZED)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Something went wrong. Please contact us.')

    def test_add_user_inactive(self):
        add_user()
        # update user
        user = User.query.filter_by(email=EMAIL).first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username=JOHN,
                    email=JOHN_EMAIL,
                    password=JOHN_PASSWORD
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            self.assertEqual(response.status_code, http_response.UNAUTHORIZED)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Something went wrong. Please contact us.')
