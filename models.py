from app import db
from datetime import datetime
import secrets
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    api_keys = db.relationship('ApiKey', backref='user', lazy=True)
    webhooks = db.relationship('Webhook', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_api_key(self, name, expires_at=None):
        api_key = ApiKey(
            key=f"bloxapi_{secrets.token_hex(16)}",
            name=name,
            user_id=self.id,
            expires_at=expires_at
        )
        db.session.add(api_key)
        db.session.commit()
        return api_key
    
    def __repr__(self):
        return f'<User {self.username}>'

class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    tier = db.Column(db.String(16), default='standard')  # standard, premium, enterprise
    last_used = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def get_rate_limit(self):
        # Повышенные лимиты для разных тарифных планов
        limits = {
            'standard': 60,    # 60 запросов в минуту (по умолчанию)
            'premium': 300,    # 300 запросов в минуту
            'enterprise': 1000  # 1000 запросов в минуту
        }
        return limits.get(self.tier, 60)
    
    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True
    
    def __repr__(self):
        return f'<ApiKey {self.name}>'

class ApiKeyUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key_id = db.Column(db.Integer, db.ForeignKey('api_key.id'), nullable=False)
    endpoint = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status_code = db.Column(db.Integer, nullable=False)
    response_time = db.Column(db.Float, nullable=False)  # в миллисекундах
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(256), nullable=True)
    
    api_key = db.relationship('ApiKey', backref='usage_logs')
    
    def __repr__(self):
        return f'<ApiKeyUsage {self.endpoint} at {self.timestamp}>'

class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True)
    name = db.Column(db.String(64), nullable=False)
    url = db.Column(db.String(256), nullable=False)
    secret = db.Column(db.String(64), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    events = db.Column(db.String(512), nullable=False, default='all')  # Comma-separated list of events or 'all'
    
    def __repr__(self):
        return f'<Webhook {self.name}>'

class WebhookDelivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    webhook_id = db.Column(db.Integer, db.ForeignKey('webhook.id'), nullable=False)
    event = db.Column(db.String(64), nullable=False)
    payload = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status_code = db.Column(db.Integer, nullable=True)
    response = db.Column(db.Text, nullable=True)
    success = db.Column(db.Boolean, default=False)
    
    webhook = db.relationship('Webhook', backref='deliveries')
    
    def __repr__(self):
        return f'<WebhookDelivery {self.event} at {self.timestamp}>'

class CacheEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    def is_valid(self):
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True
    
    def __repr__(self):
        return f'<CacheEntry {self.key}>'