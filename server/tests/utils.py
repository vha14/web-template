import datetime

from server import db
from server.models import User

NAME = 'justatest'
EMAIL = 'test@test.com'
PASSWORD = 'password'

JOHN = 'John'
JOHN_EMAIL = 'john@wayne.com'
JOHN_PASSWORD = 'password'
JANE = 'Jane'
JANE_EMAIL = 'jane@fonda.com'
JANE_PASSWORD = 'password'

TEST_USER = dict(
    username=NAME,
    email=EMAIL,
    password=PASSWORD
)


def add_user(username=NAME, email=EMAIL, password=PASSWORD, created_at=datetime.datetime.utcnow()):
    user = User(
        username=username,
        email=email,
        password=password,
        created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user
