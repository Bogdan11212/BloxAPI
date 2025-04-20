from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Resource
from app import db
from models import User, ApiKey, ApiKeyUsage
from datetime import datetime, timedelta
from functools import wraps
import secrets
from werkzeug.exceptions import Unauthorized, Forbidden

auth_bp = Blueprint('auth', __name__)

# Декоратор для проверки API-ключа
def require_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': {
                    'code': 401,
                    'message': 'API key is missing'
                }
            }), 401
        
        key = ApiKey.query.filter_by(key=api_key).first()
        
        if not key or not key.is_valid():
            return jsonify({
                'success': False,
                'error': {
                    'code': 401,
                    'message': 'Invalid or expired API key'
                }
            }), 401
        
        # Сохраняем информацию о ключе и пользователе для дальнейшего использования
        request.api_key = key
        request.user = key.user
        
        # Отслеживаем использование ключа
        key.last_used = datetime.utcnow()
        db.session.add(key)
        
        # Регистрируем использование API для аналитики
        usage = ApiKeyUsage(
            api_key_id=key.id,
            endpoint=request.path,
            status_code=200,  # Будет обновлено позже при необходимости
            response_time=0,  # Будет обновлено позже
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None
        )
        db.session.add(usage)
        db.session.commit()
        
        return func(*args, **kwargs)
    
    return decorated_function

# Декоратор для проверки прав администратора
def admin_required(func):
    @wraps(func)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Вам необходимы права администратора для доступа к этой странице.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    
    return decorated_function

# Маршруты веб-интерфейса для аутентификации
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
            return redirect(next_page)
        
        flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Проверка, не занято ли имя пользователя или email
        if User.query.filter_by(username=username).first():
            flash('Имя пользователя уже занято', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email уже зарегистрирован', 'danger')
            return render_template('auth/register.html')
        
        # Создание нового пользователя
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Первый зарегистрированный пользователь становится администратором
        if User.query.count() == 0:
            user.is_admin = True
        
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

# Маршруты для управления API-ключами через веб-интерфейс
@auth_bp.route('/profile')
@login_required
def profile():
    api_keys = ApiKey.query.filter_by(user_id=current_user.id).all()
    return render_template('auth/profile.html', api_keys=api_keys)

@auth_bp.route('/api-keys/create', methods=['GET', 'POST'])
@login_required
def create_api_key():
    if request.method == 'POST':
        name = request.form.get('name')
        expires_days = request.form.get('expires_days')
        
        if not name:
            flash('Необходимо указать имя для API-ключа', 'danger')
            return redirect(url_for('auth.create_api_key'))
        
        expires_at = None
        if expires_days and expires_days.isdigit():
            expires_at = datetime.utcnow() + timedelta(days=int(expires_days))
        
        api_key = current_user.generate_api_key(name, expires_at)
        
        flash(f'API-ключ создан. Сохраните его: {api_key.key}', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/create_api_key.html')

@auth_bp.route('/api-keys/<int:key_id>/revoke', methods=['POST'])
@login_required
def revoke_api_key(key_id):
    api_key = ApiKey.query.filter_by(id=key_id, user_id=current_user.id).first_or_404()
    api_key.is_active = False
    db.session.commit()
    
    flash('API-ключ был отозван.', 'success')
    return redirect(url_for('auth.profile'))

# API маршруты для аутентификации и управления ключами
class AuthAPI(Resource):
    def post(self):
        # API для авторизации и получения токена
        data = request.get_json()
        if not data:
            return {
                'success': False,
                'error': {
                    'code': 400,
                    'message': 'Missing JSON data'
                }
            }, 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return {
                'success': False,
                'error': {
                    'code': 400,
                    'message': 'Missing username or password'
                }
            }, 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return {
                'success': False,
                'error': {
                    'code': 401,
                    'message': 'Invalid username or password'
                }
            }, 401
        
        # Генерируем API-ключ для пользователя
        api_key = user.generate_api_key('Generated via API login')
        
        return {
            'success': True,
            'data': {
                'api_key': api_key.key,
                'expires_at': api_key.expires_at.isoformat() if api_key.expires_at else None,
                'tier': api_key.tier,
                'rate_limit': api_key.get_rate_limit()
            }
        }, 200

class ApiKeyResource(Resource):
    @require_api_key
    def get(self):
        # Проверка и получение информации о текущем API-ключе
        key = request.api_key
        
        return {
            'success': True,
            'data': {
                'key_id': key.id,
                'name': key.name,
                'created_at': key.created_at.isoformat(),
                'expires_at': key.expires_at.isoformat() if key.expires_at else None,
                'tier': key.tier,
                'rate_limit': key.get_rate_limit(),
                'last_used': key.last_used.isoformat() if key.last_used else None
            }
        }, 200
    
    @require_api_key
    def delete(self):
        # Отзыв API-ключа
        key = request.api_key
        key.is_active = False
        db.session.commit()
        
        return {
            'success': True,
            'data': {
                'message': 'API key has been revoked successfully'
            }
        }, 200

# Подключение маршрутов к API
def initialize_auth_routes(api):
    api.add_resource(AuthAPI, '/api/auth')
    api.add_resource(ApiKeyResource, '/api/auth/key')