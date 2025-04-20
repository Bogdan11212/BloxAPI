import json
import logging
import hmac
import hashlib
import time
import requests
from datetime import datetime
from threading import Thread
from flask import current_app
from app import db
from models import Webhook, WebhookDelivery

logger = logging.getLogger(__name__)

class WebhookManager:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        # Регистрируем функцию для очистки контекста приложения
        app.teardown_appcontext(self.teardown)
    
    def teardown(self, exception):
        pass
    
    def generate_signature(self, payload, secret):
        """Генерирует HMAC подпись для полезной нагрузки вебхука"""
        return hmac.new(
            secret.encode() if secret else b'',
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def send_webhook(self, webhook, event, data):
        """Отправляет вебхук на указанный URL с данными события
        
        Args:
            webhook (Webhook): Объект вебхука
            event (str): Тип события
            data (dict): Данные события для отправки
        """
        with self.app.app_context():
            # Проверяем, активен ли вебхук
            if not webhook.is_active:
                logger.warning(f"Webhook {webhook.name} is not active, skipping delivery")
                return False
            
            # Проверяем, подписан ли вебхук на это событие
            events = webhook.events.split(',')
            if 'all' not in events and event not in events:
                logger.debug(f"Webhook {webhook.name} not subscribed to event {event}, skipping")
                return False
            
            # Формируем полезную нагрузку
            payload = {
                'event': event,
                'timestamp': datetime.utcnow().isoformat(),
                'webhook_id': webhook.uuid,
                'data': data
            }
            
            payload_json = json.dumps(payload)
            
            # Вычисляем подпись, если указан секрет
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'BloxAPI-Webhook/1.0',
                'X-BloxAPI-Event': event,
                'X-BloxAPI-Delivery': webhook.uuid
            }
            
            if webhook.secret:
                signature = self.generate_signature(payload_json, webhook.secret)
                headers['X-BloxAPI-Signature'] = signature
            
            # Создаем запись о доставке в базе данных
            delivery = WebhookDelivery(
                webhook_id=webhook.id,
                event=event,
                payload=payload_json
            )
            db.session.add(delivery)
            db.session.commit()
            
            # Отправляем запрос в отдельном потоке
            thread = Thread(target=self._send_webhook_request, 
                           args=(webhook.url, headers, payload_json, delivery.id))
            thread.daemon = True
            thread.start()
            
            return True
    
    def _send_webhook_request(self, url, headers, payload, delivery_id):
        """Отправляет HTTP запрос вебхука и обновляет статус доставки
        
        Args:
            url (str): URL-адрес для отправки вебхука
            headers (dict): HTTP заголовки
            payload (str): Строка JSON-нагрузки
            delivery_id (int): ID записи доставки в базе данных
        """
        with self.app.app_context():
            try:
                start_time = time.time()
                response = requests.post(
                    url,
                    headers=headers,
                    data=payload,
                    timeout=10  # 10 секунд таймаут
                )
                elapsed_time = time.time() - start_time
                
                # Обновляем статус доставки
                delivery = WebhookDelivery.query.get(delivery_id)
                if delivery:
                    delivery.status_code = response.status_code
                    delivery.response = response.text[:1000]  # Ограничиваем длину ответа
                    delivery.success = 200 <= response.status_code < 300
                    db.session.commit()
                
                logger.info(f"Webhook delivered: URL={url}, Status={response.status_code}, Time={elapsed_time:.2f}s")
                
            except Exception as e:
                logger.error(f"Webhook delivery failed: URL={url}, Error={str(e)}")
                
                # Обновляем запись о доставке в случае ошибки
                delivery = WebhookDelivery.query.get(delivery_id)
                if delivery:
                    delivery.status_code = 0
                    delivery.response = str(e)
                    delivery.success = False
                    db.session.commit()
    
    def trigger_event(self, event, data):
        """Запускает отправку вебхуков для всех активных подписчиков на событие
        
        Args:
            event (str): Тип события
            data (dict): Данные события
        """
        with self.app.app_context():
            # Получаем все активные вебхуки
            webhooks = Webhook.query.filter_by(is_active=True).all()
            
            sent_count = 0
            for webhook in webhooks:
                if self.send_webhook(webhook, event, data):
                    sent_count += 1
            
            logger.info(f"Triggered event {event} to {sent_count} webhooks")
            return sent_count

# Создаем экземпляр менеджера вебхуков
webhook_manager = WebhookManager()