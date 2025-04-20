import os
import logging
from flask import Flask, jsonify, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration - SQLite file-based
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloxapi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Инициализация таблиц базы данных
with app.app_context():
    db.create_all()

# Create Flask-RESTful API
api = Api(app)

# Регистрация маршрутов авторизации
try:
    from routes.auth import auth_bp, initialize_auth_routes
    app.register_blueprint(auth_bp, url_prefix='/auth')
    initialize_auth_routes(api)
except ImportError:
    logger.warning("Auth routes not imported. Authentication will not be available.")

# Import routes after app is created to avoid circular imports
from routes.users import UserResource, UserBatchResource, UserSearchResource
from routes.games import GameResource, GameListResource, GameDetailsResource
from routes.groups import (
    GroupResource, GroupMembersResource, GroupRolesResource,
    GroupPayoutsResource, GroupAuditLogResource, GroupSocialsResource
)
from routes.friends import FriendsResource, FriendRequestsResource
from routes.assets import AssetResource, AssetInfoResource
from routes.catalog import CatalogResource, CatalogSearchResource

# Import new routes
from routes.avatars import (
    UserAvatarResource, UserAvatarMetaResource,
    UserOutfitsResource, OutfitDetailsResource
)
from routes.inventory import UserInventoryResource, UserCollectiblesResource
from routes.economy import (
    AssetResellersResource, AssetResaleDataResource,
    CurrencyExchangeRateResource, GroupRevenueResource, UserTransactionsResource
)
from routes.badges import (
    GameBadgesResource, BadgeInfoResource,
    BadgeAwardedDatesResource, UserBadgesResource
)
from routes.analytics import (
    GameAnalyticsResource, GamePlaytimeResource, GameRevenueAnalyticsResource
)
from routes.presence import UserPresenceResource, LastOnlineResource
from routes.thumbnails import (
    UserThumbnailsResource, AssetThumbnailsResource, GameThumbnailsResource
)
from routes.notifications import NotificationsResource, NotificationCountsResource
from routes.develop import (
    GameTeamCreateMembersResource, GamePackagesResource,
    GameCurrentVersionResource, GameVersionHistoryResource
)
from routes.chat import ChatConversationsResource, ChatMessagesResource

# Import external service integrations
from routes.external import (
    # Rolimon's routes
    RolimonItemDetailsResource, RolimonItemValuesResource,
    RolimonItemPriceHistoryResource, RolimonDealsResource,
    RolimonPlayerRapResource, RolimonPlayerValueResource,
    RolimonPlayerInventoryValueResource,
    
    # Rblx.Trade routes
    RblxTradeAdsResource, RblxTradePlayerReputationResource,
    RblxTradeValueCalculatorResource,
    
    # Roliverse routes
    RoliversePlayerTradingActivityResource, RoliverseMarketTrendsResource,
    RoliverseDemandIndexResource,
    
    # Rblx Values routes
    RblxValuesItemProjectedStatusResource, RblxValuesItemStabilityResource,
    RblxValuesRisingItemsResource, RblxValuesFallingItemsResource
)

# Register API routes
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(UserBatchResource, '/api/users')
api.add_resource(UserSearchResource, '/api/users/search')

api.add_resource(GameResource, '/api/games/<int:game_id>')
api.add_resource(GameListResource, '/api/games')
api.add_resource(GameDetailsResource, '/api/games/<int:game_id>/details')

api.add_resource(GroupResource, '/api/groups/<int:group_id>')
api.add_resource(GroupMembersResource, '/api/groups/<int:group_id>/members')
api.add_resource(GroupRolesResource, '/api/groups/<int:group_id>/roles')

api.add_resource(FriendsResource, '/api/users/<int:user_id>/friends')
api.add_resource(FriendRequestsResource, '/api/users/<int:user_id>/friend-requests')

api.add_resource(AssetResource, '/api/assets/<int:asset_id>')
api.add_resource(AssetInfoResource, '/api/assets/<int:asset_id>/info')

api.add_resource(CatalogResource, '/api/catalog')
api.add_resource(CatalogSearchResource, '/api/catalog/search')

# Register Avatar API routes
api.add_resource(UserAvatarResource, '/api/users/<int:user_id>/avatar')
api.add_resource(UserAvatarMetaResource, '/api/users/<int:user_id>/avatar/meta')
api.add_resource(UserOutfitsResource, '/api/users/<int:user_id>/outfits')
api.add_resource(OutfitDetailsResource, '/api/outfits/<int:outfit_id>')

# Register Inventory API routes
api.add_resource(UserInventoryResource, '/api/users/<int:user_id>/inventory/<string:asset_type>')
api.add_resource(UserCollectiblesResource, '/api/users/<int:user_id>/collectibles')

# Register Economy API routes
api.add_resource(AssetResellersResource, '/api/economy/assets/<int:asset_id>/resellers')
api.add_resource(AssetResaleDataResource, '/api/economy/assets/<int:asset_id>/resale-data')
api.add_resource(CurrencyExchangeRateResource, '/api/economy/currency/exchange-rate')
api.add_resource(GroupRevenueResource, '/api/economy/groups/<int:group_id>/revenue')
api.add_resource(UserTransactionsResource, '/api/economy/users/<int:user_id>/transactions/<string:transaction_type>')

# Register Badge API routes
api.add_resource(GameBadgesResource, '/api/badges/games/<int:universe_id>')
api.add_resource(BadgeInfoResource, '/api/badges/<int:badge_id>')
api.add_resource(BadgeAwardedDatesResource, '/api/badges/<int:badge_id>/user/<int:user_id>/awarded')
api.add_resource(UserBadgesResource, '/api/users/<int:user_id>/badges')

# Register Analytics API routes
api.add_resource(GameAnalyticsResource, '/api/analytics/games/<int:universe_id>/<string:metric_type>')
api.add_resource(GamePlaytimeResource, '/api/analytics/games/<int:universe_id>/playtime')
api.add_resource(GameRevenueAnalyticsResource, '/api/analytics/games/<int:universe_id>/revenue')

# Register Presence API routes
api.add_resource(UserPresenceResource, '/api/presence/users')
api.add_resource(LastOnlineResource, '/api/presence/users/last-online')

# Register Thumbnail API routes
api.add_resource(UserThumbnailsResource, '/api/thumbnails/users')
api.add_resource(AssetThumbnailsResource, '/api/thumbnails/assets')
api.add_resource(GameThumbnailsResource, '/api/thumbnails/games')

# Register Notification API routes
api.add_resource(NotificationsResource, '/api/notifications')
api.add_resource(NotificationCountsResource, '/api/notifications/counts')

# Register Development API routes
api.add_resource(GameTeamCreateMembersResource, '/api/develop/games/<int:universe_id>/team-create/members')
api.add_resource(GamePackagesResource, '/api/develop/games/<int:universe_id>/packages')
api.add_resource(GameCurrentVersionResource, '/api/develop/games/<int:universe_id>/version')
api.add_resource(GameVersionHistoryResource, '/api/develop/games/<int:universe_id>/version/history')

# Register Chat API routes
api.add_resource(ChatConversationsResource, '/api/chat/conversations')
api.add_resource(ChatMessagesResource, '/api/chat/messages')

# Register additional Group API routes
api.add_resource(GroupPayoutsResource, '/api/groups/<int:group_id>/payouts')
api.add_resource(GroupAuditLogResource, '/api/groups/<int:group_id>/audit-log')
api.add_resource(GroupSocialsResource, '/api/groups/<int:group_id>/socials')

# Register External Services API routes (RoliMon's)
api.add_resource(RolimonItemDetailsResource, '/api/external/rolimon/items/<int:item_id>')
api.add_resource(RolimonItemValuesResource, '/api/external/rolimon/items/values')
api.add_resource(RolimonItemPriceHistoryResource, '/api/external/rolimon/items/<int:item_id>/history')
api.add_resource(RolimonDealsResource, '/api/external/rolimon/deals')
api.add_resource(RolimonPlayerRapResource, '/api/external/rolimon/players/<int:user_id>/rap')
api.add_resource(RolimonPlayerValueResource, '/api/external/rolimon/players/<int:user_id>/value')
api.add_resource(RolimonPlayerInventoryValueResource, '/api/external/rolimon/players/<int:user_id>/inventory-value')

# Register External Services API routes (Rblx.Trade)
api.add_resource(RblxTradeAdsResource, '/api/external/rblx-trade/trade-ads')
api.add_resource(RblxTradePlayerReputationResource, '/api/external/rblx-trade/players/<int:user_id>/reputation')
api.add_resource(RblxTradeValueCalculatorResource, '/api/external/rblx-trade/trade-calculator')

# Register External Services API routes (Roliverse)
api.add_resource(RoliversePlayerTradingActivityResource, '/api/external/roliverse/players/<int:user_id>/trades')
api.add_resource(RoliverseMarketTrendsResource, '/api/external/roliverse/market/trends')
api.add_resource(RoliverseDemandIndexResource, '/api/external/roliverse/items/<int:item_id>/demand')

# Register External Services API routes (Rblx Values)
api.add_resource(RblxValuesItemProjectedStatusResource, '/api/external/rblx-values/items/<int:item_id>/projected')
api.add_resource(RblxValuesItemStabilityResource, '/api/external/rblx-values/items/<int:item_id>/stability')
api.add_resource(RblxValuesRisingItemsResource, '/api/external/rblx-values/market/rising')
api.add_resource(RblxValuesFallingItemsResource, '/api/external/rblx-values/market/falling')

# Web routes for documentation
@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

@app.route('/docs')
def documentation():
    from flask import render_template
    return render_template('documentation.html')

@app.route('/integrations')
def integrations():
    from flask import render_template
    return render_template('integrations.html')

# Error handling
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = jsonify({
        'success': False,
        'error': {
            'code': e.code,
            'name': e.name,
            'description': e.description,
        }
    })
    response.status_code = e.code
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception("Unhandled exception occurred")
    response = jsonify({
        'success': False,
        'error': {
            'code': 500,
            'name': 'Internal Server Error',
            'description': str(e) if app.debug else 'An unexpected error occurred',
        }
    })
    response.status_code = 500
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
