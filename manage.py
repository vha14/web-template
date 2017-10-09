import unittest

from coverage import coverage
from flask_migrate import MigrateCommand
from flask_script import Manager

from server import create_app, db
from server.models import User

COV = coverage(
    branch=True,
    include='server/*',
    omit=[
        'server/tests/*'
    ]
)
COV.start()

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('server/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    """Seeds the database."""
    from server.tests.utils import JOHN, JOHN_EMAIL, JOHN_PASSWORD
    from server.tests.utils import JANE, JANE_EMAIL, JANE_PASSWORD
    db.session.add(User(username=JOHN, email=JOHN_EMAIL, password=JOHN_PASSWORD))
    db.session.add(User(username=JANE, email=JANE_EMAIL, password=JANE_PASSWORD))
    db.session.commit()


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('server/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
