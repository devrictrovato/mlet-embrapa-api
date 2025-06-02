from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from flasgger.utils import swag_from

from db.database import db
from db.model import User

auth_routes = Blueprint('auth', __name__)


# ---------- REGISTRO ----------
@auth_routes.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Registrar novo usuário',
    'description': 'Cria um novo usuário com nome de usuário e senha.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'Usuário registrado com sucesso'},
        400: {'description': 'Usuário já existe'}
    }
})
def register():
    data = request.get_json()
    username = data.get('username')
    password = generate_password_hash(data.get('password'))

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'Usuário já existe'}), 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário registrado com sucesso'}), 201


# ---------- LOGIN ----------
@auth_routes.route('/login', methods=['GET', 'POST'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Login do usuário',
    'description': 'Autentica um usuário e retorna um token JWT.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'Token JWT retornado com sucesso'},
        401: {'description': 'Credenciais inválidas'}
    }
})
def login():
    # Se for GET, apenas renderiza a página
    if request.method == 'GET':
        return render_template('login.html')

    # POST = tentativa de login (API)
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Campos obrigatórios ausentes'}), 400

    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not check_password_hash(user.password, data.get('password')):
        return jsonify({'message': 'Credenciais inválidas'}), 401

    token = create_access_token(identity=user.username)
    return jsonify(access_token=token), 200


# ---------- ATUALIZAR SENHA ----------
@auth_routes.route('/update', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Auth'],
    'summary': 'Atualizar senha',
    'description': 'Permite ao usuário autenticado atualizar sua senha.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'new_password': {'type': 'string'}
                },
                'required': ['new_password']
            }
        }
    ],
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {'description': 'Senha atualizada com sucesso'},
        400: {'description': 'Senha inválida ou ausente'}
    }
})
def update_password():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'msg': 'Nova senha não fornecida'}), 400

    user = User.query.filter_by(username=current_user).first()
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({'msg': 'Senha atualizada com sucesso'}), 200


# ---------- DELETAR CONTA ----------
@auth_routes.route('/delete', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Auth'],
    'summary': 'Deletar conta',
    'description': 'Permite ao usuário autenticado deletar sua própria conta.',
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {'description': 'Conta deletada com sucesso'},
        404: {'description': 'Usuário não encontrado'}
    }
})
def delete_account():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({'msg': 'Usuário não encontrado'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'Conta deletada com sucesso'}), 200