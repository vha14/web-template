from flask import jsonify, request, Blueprint
from sqlalchemy import exc

from server import db
import server.http_response as http_response
from server.http_response import APIResponse
from server.models import User
from server.auth import authenticate

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users', methods=['POST'])
@authenticate
def add_user(resp) -> APIResponse:
    if not is_admin(resp):
        return jsonify({
            'status': 'error',
            'message': 'You do not have permission to do that.'
        }), http_response.UNAUTHORIZED
    post_data = request.get_json()
    if not post_data:
        return jsonify({
            'status': 'fail',
            'message': 'Invalid payload.'
        }), http_response.BAD_REQUEST
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(
                username=(post_data.get('username')),
                email=email,
                password=(post_data.get('password'))))
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': f'{email} was added!'
            }), http_response.CREATED
        else:
            return jsonify({
                'status': 'fail',
                'message': 'Sorry. That email already exists.'
            }), http_response.BAD_REQUEST
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'status': 'fail',
            'message': 'Invalid payload.'
        }), http_response.BAD_REQUEST
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify({
            'status': 'fail',
            'message': 'Invalid payload.'
        }), http_response.BAD_REQUEST


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id) -> APIResponse:
    try:
        return jsonify({
            'status': 'success',
            'data': User.query.filter_by(id=int(user_id)).first().to_json()
        }), http_response.OK
    except (ValueError, AttributeError):
        return jsonify({
            'status': 'fail',
            'message': 'User does not exist'
        }), http_response.NOT_FOUND


@users_blueprint.route('/users', methods=['GET'])
def get_all_users() -> APIResponse:
    return jsonify({
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }), http_response.OK


def is_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.admin
