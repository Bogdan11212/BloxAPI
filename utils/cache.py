import hashlib
import json
import logging
import time
from datetime import datetime, timedelta
from functools import wraps

from app import db
from models import CacheEntry

logger = logging.getLogger(__name__)

def generate_cache_key(prefix, *args, **kwargs):
    """Генерирует уникальный ключ кэша на основе аргументов функции"""
    key_parts = [prefix]
    
    for arg in args:
        key_parts.append(str(arg))
    
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}={v}")
    
    key_string = ":".join(key_parts)
    return f"bloxapi:{hashlib.md5(key_string.encode()).hexdigest()}"

def cache_result(ttl=300):
    """Декоратор для кэширования результатов API-вызовов
    
    Args:
        ttl (int): Время жизни кэша в секундах (по умолчанию 5 минут)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Генерируем ключ для этого конкретного вызова
            func_name = func.__name__
            cache_key = generate_cache_key(func_name, *args, **kwargs)
            
            # Проверяем, есть ли результат в кэше
            cache_entry = CacheEntry.query.filter_by(key=cache_key).first()
            
            # Если кэш существует и актуален, возвращаем его
            if cache_entry and cache_entry.is_valid():
                logger.debug(f"Cache hit for {func_name}")
                return json.loads(cache_entry.value)
            
            # Если кэша нет или он устарел, выполняем функцию
            logger.debug(f"Cache miss for {func_name}")
            result = func(*args, **kwargs)
            
            # Сохраняем результат в кэш
            expires_at = datetime.utcnow() + timedelta(seconds=ttl)
            
            if cache_entry:
                # Обновляем существующую запись
                cache_entry.value = json.dumps(result)
                cache_entry.timestamp = datetime.utcnow()
                cache_entry.expires_at = expires_at
            else:
                # Создаем новую запись
                cache_entry = CacheEntry(
                    key=cache_key,
                    value=json.dumps(result),
                    expires_at=expires_at
                )
                db.session.add(cache_entry)
            
            db.session.commit()
            return result
        
        return wrapper
    
    return decorator

class RateLimiter:
    """Улучшенный механизм ограничения запросов с поддержкой уровней API-ключей"""
    
    def __init__(self, default_max_calls=60, default_period=60):
        self.default_max_calls = default_max_calls
        self.default_period = default_period
        self.limits = {}
        self.timestamps = {}
        logger.debug(f"Rate limiter initialized: {default_max_calls} calls per {default_period} seconds")
    
    def wait_if_needed(self, identifier="default", max_calls=None, period=None):
        """Проверяет и при необходимости ожидает, если достигнут лимит запросов
        
        Args:
            identifier (str): Уникальный идентификатор (например, IP или API-ключ)
            max_calls (int): Максимальное количество запросов (переопределение)
            period (int): Период в секундах (переопределение)
        """
        max_calls = max_calls or self.default_max_calls
        period = period or self.default_period
        
        # Инициализация лимита, если он не существует
        if identifier not in self.limits:
            self.limits[identifier] = max_calls
            self.timestamps[identifier] = []
        
        # Текущее время
        now = time.time()
        
        # Очистка устаревших временных меток
        self.timestamps[identifier] = [t for t in self.timestamps[identifier] if now - t < period]
        
        # Если достигнут лимит
        if len(self.timestamps[identifier]) >= self.limits[identifier]:
            # Вычисляем время ожидания
            wait_time = period - (now - self.timestamps[identifier][0])
            logger.warning(f"Rate limit reached for {identifier}. Waiting {wait_time:.2f} seconds.")
            time.sleep(wait_time)
            
            # Обновляем временные метки после ожидания
            self.timestamps[identifier] = [t for t in self.timestamps[identifier] if time.time() - t < period]
        
        # Добавляем текущую временную метку
        self.timestamps[identifier].append(time.time())
    
    def update_limits(self, identifier, max_calls):
        """Обновляет лимиты для конкретного идентификатора"""
        self.limits[identifier] = max_calls
        logger.debug(f"Updated rate limit for {identifier}: {max_calls} calls per {self.default_period} seconds")

def clear_expired_cache():
    """Очищает просроченные записи кэша"""
    now = datetime.utcnow()
    expired_entries = CacheEntry.query.filter(CacheEntry.expires_at < now).all()
    
    if expired_entries:
        for entry in expired_entries:
            db.session.delete(entry)
        
        db.session.commit()
        logger.info(f"Cleared {len(expired_entries)} expired cache entries")

# Создаем экземпляр ограничителя запросов
rate_limiter = RateLimiter()