import datetime
from functools import wraps
from typing import Callable

import jwt
from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import exc, or_

from server import bcrypt, db
import server.http_response as http_response
from server.http_response import APIResponse
from server.models import User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user() -> APIResponse:
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid payload.'
        }), http_response.BAD_REQUEST
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email == email)).first()
        if not user:
            # add new user to db
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': encode_auth_token(new_user.id).decode()
            }), http_response.CREATED
        else:
            return jsonify({
                'status': 'error',
                'message': 'Sorry. That user already exists.'
            }), http_response.BAD_REQUEST
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Invalid payload.'
        }), http_response.BAD_REQUEST


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user() -> APIResponse:
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            'status': 'error',
            'message': 'Invalid payload.'
        }), http_response.BAD_REQUEST
    try:
        user = User.query.filter_by(email=post_data.get('email')).first()
        if user and bcrypt.check_password_hash(user.password, post_data.get('password')):
            return jsonify({
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': encode_auth_token(user.id).decode()
            }), http_response.OK
        else:
            return jsonify({
                'status': 'error',
                'message': 'User does not exist.'
            }), http_response.NOT_FOUND
    except Exception as e:
        print(e)
        return jsonify({
            'status': 'error',
            'message': 'Try again.'
        }), http_response.INTERNAL_SERVER_ERROR


def authenticate(f: Callable[..., APIResponse]) -> Callable[..., APIResponse]:
    @wraps(f)
    def decorated_function(*args, **kwargs) -> APIResponse:
        response_object = {
            'status': 'error',
            'message': 'Something went wrong. Please contact us.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response_object['message'] = 'Provide a valid auth token.'
            return jsonify(response_object), http_response.FORBIDDEN
        auth_token = auth_header.split(" ")[1]
        try:
            resp = decode_auth_token(auth_token)
            user = User.query.filter_by(id=resp).first()
            if not user or not user.active:
                return jsonify(response_object), http_response.UNAUTHORIZED
            return f(resp, *args, **kwargs)
        except Exception as e:
            response_object['message'] = type(e).__name__
            return jsonify(response_object), http_response.UNAUTHORIZED
    return decorated_function


@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user(resp) -> APIResponse:
    return jsonify({
        'status': 'success',
        'message': 'Successfully logged out.'
    }), http_response.OK


@auth_blueprint.route('/auth/status', methods=['GET'])
@authenticate
def get_user_status(resp) -> APIResponse:
    return jsonify({
        'status': 'success',
        'data': User.query.filter_by(id=resp).first().to_json()
    }), http_response.OK


def encode_auth_token(user_id) -> bytes:
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
            seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
        ),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )


def decode_auth_token(auth_token) -> int:
    return jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))['sub']
