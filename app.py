import os
import logging
from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Create Flask-RESTful API
api = Api(app)

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

# Web routes for documentation
@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

@app.route('/docs')
def documentation():
    from flask import render_template
    return render_template('documentation.html')

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
