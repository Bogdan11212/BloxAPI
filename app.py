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

# Import new advanced modules
from routes.events import (
    UserEventsResource, GameEventsResource, GroupEventsResource,
    EventHistoryResource, EventDetailsResource
)
from routes.moderation import (
    ContentModerationStatusResource, ModerationHistoryResource,
    AssetModerationCheckResource, TextModerationCheckResource,
    ImageModerationCheckResource, ReportAbuseResource, SafetySettingsResource
)
from routes.monetization import (
    DeveloperProductsResource, DeveloperProductDetailsResource,
    GamePassesResource, GamePassDetailsResource, PremiumPayoutsResource,
    TransactionHistoryResource, SalesSummaryResource, RevenueSummaryResource,
    ProductPurchasesResource, PlayerOwnershipResource
)
from routes.social import (
    SocialConnectionsResource, SocialLinksResource, FollowersResource,
    FollowingsResource, SubscribersResource, SubscriptionsResource,
    FollowerStatusResource, FollowingStatusResource,
    FriendRecommendationsResource, SocialGraphResource, AccountRelationshipResource
)
from routes.statistics import (
    GameUniverseStatsResource, GameVersionHistoryStatsResource,
    GamePlaytimeStatsResource, GameRetentionStatsResource,
    GamePerformanceStatsResource, GameDeviceStatsResource,
    GameDemographicStatsResource, GameGeographicStatsResource,
    GameConversionStatsResource, PlayerActivityStatsResource,
    TrendingGamesResource, GameComparisonStatsResource
)
from routes.servers import (
    GameServerInstancesResource, ServerDetailsResource,
    ServerPlayersResource, ServerStatsResource, ServerLogsResource,
    ServerMessageResource, ServerShutdownResource, ServerJoinScriptResource,
    VipServersResource, CreateVipServerResource, UpdateVipServerResource,
    VipServerSubscribersResource, PrivateServersResource
)
from routes.subscriptions import (
    UserSubscriptionsResource, UserSubscribersResource,
    UserSubscriptionDetailsResource, SubscriptionOptionsResource,
    SubscriptionStatusResource, SubscriptionNotificationsResource,
    SubscriptionFeedResource
)
from routes.user_profiles import (
    UserStatusResource, UserBiographyResource, UserDisplayNameResource,
    UserPremiumStatusResource, UserProfilePresenceResource, UserOnlineStatusResource,
    UserProfileBadgesResource, UserMembershipTypeResource,
    UserPreviousUsernamesResource, UserAgeResource, UserJoinDateResource,
    UserDisplayNameHistoryResource, SearchUsersByDisplayNameResource,
    UserConnectionsResource, UserProfileThemeResource, UserRobloxBadgesResource
)

# Import new security API modules
from routes.security import (
    SecuritySettingsResource, SecurityActivityLogResource,
    AccountLockStatusResource, EmailVerificationStatusResource,
    PhoneVerificationStatusResource, TwoStepVerificationResource,
    DeviceVerificationResource, PasswordResetResource,
    AccountRestrictionsResource, AccountRiskAssessmentResource
)

# Import new developer platform API modules
from routes.developer_platform import (
    ApiKeysResource, ApiKeyUsageResource, WebhooksResource,
    WebhookDeliveryHistoryResource, DeveloperForumsResource,
    DeveloperForumPostsResource, DeveloperExchangeResource,
    DeveloperToolsUsageResource, DeveloperAnalyticsConfigResource,
    DeveloperStatsResource
)

# Import new marketplace API modules
from routes.marketplace import (
    MarketplaceItemsResource, MarketplaceItemDetailsResource,
    MarketplaceSimilarItemsResource, MarketplaceItemCommentsResource,
    MarketplaceItemRecommendationsResource, MarketplaceBundlesResource,
    MarketplaceBundleDetailsResource, MarketplaceFeaturedItemsResource,
    MarketplacePriceHistoryResource, MarketplaceSalesResource
)

# Import new content creation API modules
from routes.content_creation import (
    ContentTemplatesResource, ContentTemplateDetailsResource,
    ContentTemplateReviewsResource, AssetCreationResource,
    AssetLibraryResource, AssetDetailsResource,
    AssetTagsResource, AssetVersionsResource, AssetStatsResource
)

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

# Register Events API routes
api.add_resource(UserEventsResource, '/api/events/users/<int:user_id>')
api.add_resource(GameEventsResource, '/api/events/games/<int:universe_id>')
api.add_resource(GroupEventsResource, '/api/events/groups/<int:group_id>')
api.add_resource(EventHistoryResource, '/api/events/history/<string:entity_type>/<int:entity_id>')
api.add_resource(EventDetailsResource, '/api/events/<int:event_id>')

# Register Moderation API routes
api.add_resource(ContentModerationStatusResource, '/api/moderation/content/<string:content_type>/<int:content_id>')
api.add_resource(ModerationHistoryResource, '/api/moderation/users/<int:user_id>/history')
api.add_resource(AssetModerationCheckResource, '/api/moderation/assets/<int:asset_id>')
api.add_resource(TextModerationCheckResource, '/api/moderation/text')
api.add_resource(ImageModerationCheckResource, '/api/moderation/image')
api.add_resource(ReportAbuseResource, '/api/moderation/report')
api.add_resource(SafetySettingsResource, '/api/moderation/users/<int:user_id>/safety-settings')

# Register Monetization API routes
api.add_resource(DeveloperProductsResource, '/api/monetization/games/<int:universe_id>/developer-products')
api.add_resource(DeveloperProductDetailsResource, '/api/monetization/developer-products/<int:product_id>')
api.add_resource(GamePassesResource, '/api/monetization/games/<int:universe_id>/game-passes')
api.add_resource(GamePassDetailsResource, '/api/monetization/game-passes/<int:pass_id>')
api.add_resource(PremiumPayoutsResource, '/api/monetization/games/<int:universe_id>/premium-payouts')
api.add_resource(TransactionHistoryResource, '/api/monetization/games/<int:universe_id>/transactions')
api.add_resource(SalesSummaryResource, '/api/monetization/games/<int:universe_id>/sales-summary')
api.add_resource(RevenueSummaryResource, '/api/monetization/games/<int:universe_id>/revenue-summary')
api.add_resource(ProductPurchasesResource, '/api/monetization/games/<int:universe_id>/products/<int:product_id>/purchases')
api.add_resource(PlayerOwnershipResource, '/api/monetization/users/<int:user_id>/ownership/<string:asset_type>/<int:asset_id>')

# Register Social API routes
api.add_resource(SocialConnectionsResource, '/api/social/users/<int:user_id>/connections')
api.add_resource(SocialLinksResource, '/api/social/users/<int:user_id>/links')
api.add_resource(FollowersResource, '/api/social/users/<int:user_id>/followers')
api.add_resource(FollowingsResource, '/api/social/users/<int:user_id>/followings')
api.add_resource(SubscribersResource, '/api/social/users/<int:user_id>/subscribers')
api.add_resource(SubscriptionsResource, '/api/social/users/<int:user_id>/subscriptions')
api.add_resource(FollowerStatusResource, '/api/social/users/<int:user_id>/followers/<int:follower_id>/status')
api.add_resource(FollowingStatusResource, '/api/social/users/<int:user_id>/followings/<int:following_id>/status')
api.add_resource(FriendRecommendationsResource, '/api/social/users/<int:user_id>/friend-recommendations')
api.add_resource(SocialGraphResource, '/api/social/users/<int:user_id>/graph')
api.add_resource(AccountRelationshipResource, '/api/social/users/<int:user_id>/relationship/<int:other_user_id>')

# Register Statistics API routes
api.add_resource(GameUniverseStatsResource, '/api/statistics/games/<int:universe_id>/universe')
api.add_resource(GameVersionHistoryStatsResource, '/api/statistics/games/<int:universe_id>/version-history')
api.add_resource(GamePlaytimeStatsResource, '/api/statistics/games/<int:universe_id>/playtime')
api.add_resource(GameRetentionStatsResource, '/api/statistics/games/<int:universe_id>/retention')
api.add_resource(GamePerformanceStatsResource, '/api/statistics/games/<int:universe_id>/performance')
api.add_resource(GameDeviceStatsResource, '/api/statistics/games/<int:universe_id>/devices')
api.add_resource(GameDemographicStatsResource, '/api/statistics/games/<int:universe_id>/demographics')
api.add_resource(GameGeographicStatsResource, '/api/statistics/games/<int:universe_id>/geographic')
api.add_resource(GameConversionStatsResource, '/api/statistics/games/<int:universe_id>/conversion')
api.add_resource(PlayerActivityStatsResource, '/api/statistics/users/<int:user_id>/activity')
api.add_resource(TrendingGamesResource, '/api/statistics/games/trending')
api.add_resource(GameComparisonStatsResource, '/api/statistics/games/compare')

# Register Servers API routes
api.add_resource(GameServerInstancesResource, '/api/servers/games/<int:universe_id>/instances')
api.add_resource(ServerDetailsResource, '/api/servers/<string:server_id>')
api.add_resource(ServerPlayersResource, '/api/servers/<string:server_id>/players')
api.add_resource(ServerStatsResource, '/api/servers/<string:server_id>/stats')
api.add_resource(ServerLogsResource, '/api/servers/<string:server_id>/logs')
api.add_resource(ServerMessageResource, '/api/servers/<string:server_id>/message')
api.add_resource(ServerShutdownResource, '/api/servers/<string:server_id>/shutdown')
api.add_resource(ServerJoinScriptResource, '/api/servers/<string:server_id>/join-script')
api.add_resource(VipServersResource, '/api/servers/games/<int:universe_id>/vip')
api.add_resource(CreateVipServerResource, '/api/servers/games/<int:universe_id>/vip/create')
api.add_resource(UpdateVipServerResource, '/api/servers/vip/<string:server_id>')
api.add_resource(VipServerSubscribersResource, '/api/servers/vip/<string:server_id>/subscribers')
api.add_resource(PrivateServersResource, '/api/servers/users/<int:user_id>/private')

# Register Subscriptions API routes
api.add_resource(UserSubscriptionsResource, '/api/subscriptions/users/<int:user_id>/subscriptions')
api.add_resource(UserSubscribersResource, '/api/subscriptions/users/<int:user_id>/subscribers')
api.add_resource(UserSubscriptionDetailsResource, '/api/subscriptions/users/<int:user_id>/subscriptions/<int:subscription_id>')
api.add_resource(SubscriptionOptionsResource, '/api/subscriptions/options/<string:entity_type>/<int:entity_id>')
api.add_resource(SubscriptionStatusResource, '/api/subscriptions/users/<int:user_id>/status/<string:entity_type>/<int:entity_id>')
api.add_resource(SubscriptionNotificationsResource, '/api/subscriptions/users/<int:user_id>/notifications')
api.add_resource(SubscriptionFeedResource, '/api/subscriptions/users/<int:user_id>/feed')

# Register User Profiles API routes
api.add_resource(UserStatusResource, '/api/user-profiles/<int:user_id>/status')
api.add_resource(UserBiographyResource, '/api/user-profiles/<int:user_id>/biography')
api.add_resource(UserDisplayNameResource, '/api/user-profiles/<int:user_id>/display-name')
api.add_resource(UserPremiumStatusResource, '/api/user-profiles/<int:user_id>/premium-status')
api.add_resource(UserProfilePresenceResource, '/api/user-profiles/<int:user_id>/presence')
api.add_resource(UserOnlineStatusResource, '/api/user-profiles/<int:user_id>/online-status')
api.add_resource(UserProfileBadgesResource, '/api/user-profiles/<int:user_id>/badges')
api.add_resource(UserMembershipTypeResource, '/api/user-profiles/<int:user_id>/membership-type')
api.add_resource(UserPreviousUsernamesResource, '/api/user-profiles/<int:user_id>/previous-usernames')
api.add_resource(UserAgeResource, '/api/user-profiles/<int:user_id>/age')
api.add_resource(UserJoinDateResource, '/api/user-profiles/<int:user_id>/join-date')
api.add_resource(UserDisplayNameHistoryResource, '/api/user-profiles/<int:user_id>/display-name-history')
api.add_resource(SearchUsersByDisplayNameResource, '/api/user-profiles/search-by-display-name')
api.add_resource(UserConnectionsResource, '/api/user-profiles/<int:user_id>/connections')
api.add_resource(UserProfileThemeResource, '/api/user-profiles/<int:user_id>/theme')
api.add_resource(UserRobloxBadgesResource, '/api/user-profiles/<int:user_id>/roblox-badges')

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
