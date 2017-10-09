#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

test_requirements = [
    'alembic==0.9.5'
    'bcrypt==3.1.3'
    'cffi==1.11.0'
    'click==6.7'
    'coverage==4.4.1'
    'Flask==0.12'
    'Flask-Bcrypt==0.7.1'
    'Flask-Cors==3.0.2'
    'Flask-Migrate==2.0.4'
    'Flask-Script==2.0.6'
    'Flask-SQLAlchemy==2.2'
    'Flask-Testing==0.6.2'
    'gunicorn==19.7.1'
    'itsdangerous==0.24'
    'Jinja2==2.9.6'
    'livereload==2.5.1'
    'Mako==1.0.7'
    'MarkupSafe==1.0'
    'psycopg2==2.7.3'
    'py==1.4.34'
    'pycparser==2.18'
    'PyJWT==1.5.0'
    'pytest==3.2.2'
    'python-dateutil==2.6.1'
    'python-editor==1.0.3'
    'six==1.10.0'
    'SQLAlchemy==1.1.14'
    'tornado==4.5.2'
    'Werkzeug==0.12.2'
]

setup(
    name='webapp-template',
    version='0.1',
    test_require=test_requirements,
    url='https://github.com/allenai/webapp-template',
    license='Apache Software License 2.0',
    author='Allen AI',
    author_email='vuh@allenai.org',
    description='Webapp template with flask, reactjs, nginx, postgres, and docker'
)
