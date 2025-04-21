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

# Import new advanced analytics modules
from routes.advanced_analytics import (
    UserRetentionAnalyticsResource, UserAcquisitionAnalyticsResource,
    UserEngagementAnalyticsResource, UserLifetimeValueResource,
    DeveloperFunnelAnalyticsResource, SessionLengthDistributionResource,
    SessionFrequencyAnalyticsResource, SessionIntervalAnalyticsResource,
    PlayerSegmentationResource, CustomEventAnalyticsResource,
    FunnelConversionAnalyticsResource, PlayerCohortAnalyticsResource,
    PlayerAttributionAnalyticsResource, AbTestAnalyticsResource,
    PlayerPredictionResource, FeatureImpactAnalyticsResource,
    PlayerPatternAnalyticsResource
)

# Import localization modules
from routes.localization import (
    SupportedLanguagesResource, GameTextTranslationsResource,
    GameInterfaceTranslationsResource, AutoTranslationResource,
    LocalizationStatsResource, LocalizationQualityResource,
    LocalizationMissingTermsResource, LocalizationContributorsResource,
    LocalizationScheduleResource, LocalizationRegionalSettingsResource,
    LocalizationGlossaryResource, LocalizationMetricsResource,
    LocalizationFeedbackResource, LocalizationReportsResource,
    LocalizationExportResource, LocalizationImportResource,
    LocalizationWorkflowResource, LocalizationServiceProvidersResource,
    LocalizationStyleGuideResource
)

# Import AI services modules
from routes.ai_services import (
    TextGenerationResource, DialogueGenerationResource,
    NpcBehaviorGenerationResource, WorldBuildingResource,
    StoryGenerationResource, QuestGenerationResource,
    PuzzleGenerationResource, ImagePromptGenerationResource,
    ContentModerationResource, SentimentAnalysisResource,
    TextSummaryResource, ChatCompletionResource,
    TextClassificationResource, NameGenerationResource,
    AiModelsResource, AiModelDetailsResource,
    AiUsageLimitsResource, AiPersonalityCreationResource,
    AiTrainingResource
)

# Import user content modules
from routes.user_content import (
    UserCreationsResource, UserShowcaseResource,
    UserPortfolioResource, UserFavoriteGamesResource,
    UserFavoriteGroupsResource, UserFavoriteAssetsResource,
    UserCollectionsResource, UserCollectionDetailsResource,
    UserContentRecommendationsResource, UserFeedResource,
    UserPostsResource, UserActivityResource,
    UserReviewsResource, UserRatingsResource,
    UserCommentsResource, UserRecentContentResource,
    UserTrendingContentResource, UserPopularContentResource,
    UserContentEngagementResource
)

# Import physics modules
from routes.physics import (
    PhysicsSettingsResource, PhysicsPerformanceStatsResource,
    PhysicsCollisionGroupsResource, PhysicsConstraintsResource,
    PhysicsMaterialsResource, PhysicsPropertiesResource,
    PhysicsJointsResource, PhysicsAssemblyResource,
    PhysicsSimulationResource, PhysicsRaycastResource,
    PhysicsVolumeResource, PhysicsParticleEmittersResource,
    PhysicsExplosionsResource, PhysicsForcesResource
)

# Import education modules
from routes.education import (
    EducationProviderResource, EducationProviderDetailsResource,
    EducationCurriculumResource, EducationCourseResource,
    EducationLessonResource, EducationProgressResource,
    EducationAssignmentResource, EducationAssignmentDetailsResource,
    EducationClassResource, EducationClassRosterResource,
    EducationEnrollmentResource, EducationCertificateResource,
    EducationCertificateDetailsResource, EducationProjectResource,
    EducationProjectDetailsResource, EducationResourcesResource,
    EducationResourceDetailsResource, EducationStandardsResource,
    EducationStandardDetailsResource
)

# Import metaverse modules
from routes.metaverse import (
    MetaverseEnvironmentsResource, MetaverseEnvironmentDetailsResource,
    MetaversePortalsResource, MetaversePortalDetailsResource,
    MetaverseAvatarsResource, MetaverseAvatarDetailsResource,
    MetaverseObjectsResource, MetaverseObjectDetailsResource,
    MetaverseEventsResource, MetaverseEventDetailsResource,
    MetaverseEnvironmentStateResource, MetaverseInteractionsResource,
    MetaverseInteractionDetailsResource, MetaversePerformanceResource,
    MetaverseUserPresenceResource, MetaverseUserPresenceHistoryResource,
    MetaverseMapResource, MetaverseNavMeshResource,
    MetaversePathfindingResource
)

# Import VR/AR modules
from routes.vr import (
    VrCompatibleGamesResource, VrGameDetailsResource,
    VrDeviceCompatibilityResource, VrControlsResource,
    VrSettingsResource, VrPlaytimeResource,
    VrPerformanceResource, VrEventsResource,
    VrEventDetailsResource, VrTutorialsResource,
    VrTutorialDetailsResource, ArCompatibleGamesResource,
    ArGameDetailsResource, ArDeviceCompatibilityResource,
    ArControlsResource, ArSettingsResource,
    ArPlaytimeResource
)

# Import cloud modules
from routes.cloud import (
    CloudServicesResource, CloudServiceDetailsResource,
    CloudStorageResource, CloudStorageItemResource,
    CloudDatabaseResource, CloudDatabaseTablesResource,
    CloudDatabaseTableDetailsResource, CloudFunctionsResource,
    CloudFunctionDetailsResource, CloudFunctionLogsResource,
    CloudFunctionMetricsResource, CloudMessagingResource,
    CloudMessagingTopicsResource, CloudMessagingTopicDetailsResource,
    CloudMessagingSubscriptionsResource, CloudMessagingSubscriptionDetailsResource,
    CloudAnalyticsResource, CloudAnalyticsEventTypesResource,
    CloudAnalyticsEventDetailsResource
)

# Import UGC modules
from routes.ugc import (
    UgcCreatorsResource, UgcCreatorDetailsResource,
    UgcCreatorItemsResource, UgcCreatorStatsResource,
    UgcItemsResource, UgcItemDetailsResource,
    UgcItemStatsResource, UgcItemReviewsResource,
    UgcItemCommentsResource, UgcItemSalesResource,
    UgcItemOwnersResource, UgcItemSimilarResource,
    UgcItemFavoritesResource, UgcItemVersionsResource,
    UgcItemVersionDetailsResource, UgcCategoriesResource,
    UgcCategoryDetailsResource, UgcTrendingItemsResource
)

# Import Integrated Analytics modules
from routes.integrated_analytics import (
    CrossPlatformAnalyticsResource, DeviceTypeAnalyticsResource,
    GeographicAnalyticsResource, AgeGroupAnalyticsResource,
    MonetizationAnalyticsResource, RetentionCohortsResource,
    AcquisitionSourcesResource, PlayerJourneyResource,
    EngagementMetricsResource, SocialInteractionsResource,
    FeatureUsageResource, ChurnPredictionResource,
    UserSegmentPerformanceResource, CompetitorAnalysisResource,
    TrendAnalysisResource, CustomDashboardResource,
    RealTimeMetricsResource
)

# Import Caching and Performance modules
from routes.caching import (
    CacheConfigurationResource, CacheStatisticsResource,
    CacheInvalidationResource, CachePreheatResource,
    PerformanceMetricsResource, ApiLatencyResource,
    ErrorRateResource, RateLimitStatsResource,
    CdnConfigurationResource, CdnPurgeResource,
    CdnAnalyticsResource, BandwidthUsageResource,
    RequestDistributionResource, LoadBalancerConfigResource,
    LoadBalancerStatsResource, GlobalDistributionResource
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

# Register Security API routes
api.add_resource(SecuritySettingsResource, '/api/security/<int:user_id>/settings')
api.add_resource(SecurityActivityLogResource, '/api/security/<int:user_id>/activity-log')
api.add_resource(AccountLockStatusResource, '/api/security/<int:user_id>/account-lock')
api.add_resource(EmailVerificationStatusResource, '/api/security/<int:user_id>/email-verification')
api.add_resource(PhoneVerificationStatusResource, '/api/security/<int:user_id>/phone-verification')
api.add_resource(TwoStepVerificationResource, '/api/security/<int:user_id>/two-step-verification')
api.add_resource(DeviceVerificationResource, '/api/security/<int:user_id>/device-verification')
api.add_resource(PasswordResetResource, '/api/security/password-reset/<string:verification_token>')
api.add_resource(AccountRestrictionsResource, '/api/security/<int:user_id>/restrictions')
api.add_resource(AccountRiskAssessmentResource, '/api/security/<int:user_id>/risk-assessment')

# Register Developer Platform API routes
api.add_resource(ApiKeysResource, '/api/developer-platform/<int:user_id>/api-keys')
api.add_resource(ApiKeyUsageResource, '/api/developer-platform/api-keys/<string:key_id>/usage')
api.add_resource(WebhooksResource, '/api/developer-platform/<int:user_id>/webhooks')
api.add_resource(WebhookDeliveryHistoryResource, '/api/developer-platform/webhooks/<string:webhook_id>/history')
api.add_resource(DeveloperForumsResource, '/api/developer-platform/<int:user_id>/forums')
api.add_resource(DeveloperForumPostsResource, '/api/developer-platform/<int:user_id>/forum-posts')
api.add_resource(DeveloperExchangeResource, '/api/developer-platform/<int:user_id>/devex')
api.add_resource(DeveloperToolsUsageResource, '/api/developer-platform/<int:user_id>/tools-usage')
api.add_resource(DeveloperAnalyticsConfigResource, '/api/developer-platform/games/<int:universe_id>/analytics-config')
api.add_resource(DeveloperStatsResource, '/api/developer-platform/<int:user_id>/stats')

# Register Marketplace API routes
api.add_resource(MarketplaceItemsResource, '/api/marketplace/items')
api.add_resource(MarketplaceItemDetailsResource, '/api/marketplace/items/<int:item_id>')
api.add_resource(MarketplaceSimilarItemsResource, '/api/marketplace/items/<int:item_id>/similar')
api.add_resource(MarketplaceItemCommentsResource, '/api/marketplace/items/<int:item_id>/comments')
api.add_resource(MarketplaceItemRecommendationsResource, '/api/marketplace/users/<int:user_id>/recommendations')
api.add_resource(MarketplaceBundlesResource, '/api/marketplace/bundles')
api.add_resource(MarketplaceBundleDetailsResource, '/api/marketplace/bundles/<int:bundle_id>')
api.add_resource(MarketplaceFeaturedItemsResource, '/api/marketplace/featured')
api.add_resource(MarketplacePriceHistoryResource, '/api/marketplace/items/<int:item_id>/price-history')
api.add_resource(MarketplaceSalesResource, '/api/marketplace/items/<int:item_id>/sales')

# Register Content Creation API routes
api.add_resource(ContentTemplatesResource, '/api/content-creation/templates')
api.add_resource(ContentTemplateDetailsResource, '/api/content-creation/templates/<string:template_id>')
api.add_resource(ContentTemplateReviewsResource, '/api/content-creation/templates/<string:template_id>/reviews')
api.add_resource(AssetCreationResource, '/api/content-creation/users/<int:user_id>/stats')
api.add_resource(AssetLibraryResource, '/api/content-creation/users/<int:user_id>/assets')
api.add_resource(AssetDetailsResource, '/api/content-creation/assets/<int:asset_id>')
api.add_resource(AssetTagsResource, '/api/content-creation/tags')
api.add_resource(AssetVersionsResource, '/api/content-creation/assets/<int:asset_id>/versions')
api.add_resource(AssetStatsResource, '/api/content-creation/assets/<int:asset_id>/stats')

# Register Advanced Analytics API routes
api.add_resource(UserRetentionAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/user-retention')
api.add_resource(UserAcquisitionAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/user-acquisition')
api.add_resource(UserEngagementAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/user-engagement')
api.add_resource(UserLifetimeValueResource, '/api/advanced-analytics/games/<int:universe_id>/user-ltv')
api.add_resource(DeveloperFunnelAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/funnel')
api.add_resource(SessionLengthDistributionResource, '/api/advanced-analytics/games/<int:universe_id>/session-length')
api.add_resource(SessionFrequencyAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/session-frequency')
api.add_resource(SessionIntervalAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/session-interval')
api.add_resource(PlayerSegmentationResource, '/api/advanced-analytics/games/<int:universe_id>/player-segments')
api.add_resource(CustomEventAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/events/<string:event_name>')
api.add_resource(FunnelConversionAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/funnel-conversion')
api.add_resource(PlayerCohortAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/player-cohorts')
api.add_resource(PlayerAttributionAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/player-attribution')
api.add_resource(AbTestAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/ab-tests/<string:test_id>')
api.add_resource(PlayerPredictionResource, '/api/advanced-analytics/games/<int:universe_id>/predictions/<string:prediction_type>')
api.add_resource(FeatureImpactAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/features/<string:feature_id>/impact')
api.add_resource(PlayerPatternAnalyticsResource, '/api/advanced-analytics/games/<int:universe_id>/player-patterns')

# Register Localization API routes
api.add_resource(SupportedLanguagesResource, '/api/localization/languages')
api.add_resource(GameTextTranslationsResource, '/api/localization/games/<int:universe_id>/text')
api.add_resource(GameInterfaceTranslationsResource, '/api/localization/games/<int:universe_id>/interface')
api.add_resource(AutoTranslationResource, '/api/localization/auto-translate')
api.add_resource(LocalizationStatsResource, '/api/localization/games/<int:universe_id>/stats')
api.add_resource(LocalizationQualityResource, '/api/localization/games/<int:universe_id>/quality')
api.add_resource(LocalizationMissingTermsResource, '/api/localization/games/<int:universe_id>/missing-terms')
api.add_resource(LocalizationContributorsResource, '/api/localization/games/<int:universe_id>/contributors')
api.add_resource(LocalizationScheduleResource, '/api/localization/games/<int:universe_id>/schedule')
api.add_resource(LocalizationRegionalSettingsResource, '/api/localization/games/<int:universe_id>/regional-settings')
api.add_resource(LocalizationGlossaryResource, '/api/localization/games/<int:universe_id>/glossary')
api.add_resource(LocalizationMetricsResource, '/api/localization/games/<int:universe_id>/metrics')
api.add_resource(LocalizationFeedbackResource, '/api/localization/games/<int:universe_id>/feedback')
api.add_resource(LocalizationReportsResource, '/api/localization/games/<int:universe_id>/reports')
api.add_resource(LocalizationExportResource, '/api/localization/games/<int:universe_id>/export')
api.add_resource(LocalizationImportResource, '/api/localization/games/<int:universe_id>/import')
api.add_resource(LocalizationWorkflowResource, '/api/localization/games/<int:universe_id>/workflow')
api.add_resource(LocalizationServiceProvidersResource, '/api/localization/service-providers')
api.add_resource(LocalizationStyleGuideResource, '/api/localization/games/<int:universe_id>/style-guide')

# Register AI Services API routes
api.add_resource(TextGenerationResource, '/api/ai/text-generation')
api.add_resource(DialogueGenerationResource, '/api/ai/dialogue-generation')
api.add_resource(NpcBehaviorGenerationResource, '/api/ai/npc-behavior')
api.add_resource(WorldBuildingResource, '/api/ai/world-building')
api.add_resource(StoryGenerationResource, '/api/ai/story-generation')
api.add_resource(QuestGenerationResource, '/api/ai/quest-generation')
api.add_resource(PuzzleGenerationResource, '/api/ai/puzzle-generation')
api.add_resource(ImagePromptGenerationResource, '/api/ai/image-prompt')
api.add_resource(ContentModerationResource, '/api/ai/content-moderation')
api.add_resource(SentimentAnalysisResource, '/api/ai/sentiment-analysis')
api.add_resource(TextSummaryResource, '/api/ai/text-summary')
api.add_resource(ChatCompletionResource, '/api/ai/chat-completion')
api.add_resource(TextClassificationResource, '/api/ai/text-classification')
api.add_resource(NameGenerationResource, '/api/ai/name-generation')
api.add_resource(AiModelsResource, '/api/ai/models')
api.add_resource(AiModelDetailsResource, '/api/ai/models/<string:model_id>')
api.add_resource(AiUsageLimitsResource, '/api/ai/usage-limits')
api.add_resource(AiPersonalityCreationResource, '/api/ai/personality-creation')
api.add_resource(AiTrainingResource, '/api/ai/training')

# Register User Content API routes
api.add_resource(UserCreationsResource, '/api/user-content/<int:user_id>/creations')
api.add_resource(UserShowcaseResource, '/api/user-content/<int:user_id>/showcase')
api.add_resource(UserPortfolioResource, '/api/user-content/<int:user_id>/portfolio')
api.add_resource(UserFavoriteGamesResource, '/api/user-content/<int:user_id>/favorite-games')
api.add_resource(UserFavoriteGroupsResource, '/api/user-content/<int:user_id>/favorite-groups')
api.add_resource(UserFavoriteAssetsResource, '/api/user-content/<int:user_id>/favorite-assets')
api.add_resource(UserCollectionsResource, '/api/user-content/<int:user_id>/collections')
api.add_resource(UserCollectionDetailsResource, '/api/user-content/<int:user_id>/collections/<string:collection_id>')
api.add_resource(UserContentRecommendationsResource, '/api/user-content/<int:user_id>/recommendations')
api.add_resource(UserFeedResource, '/api/user-content/<int:user_id>/feed')
api.add_resource(UserPostsResource, '/api/user-content/<int:user_id>/posts')
api.add_resource(UserActivityResource, '/api/user-content/<int:user_id>/activity')
api.add_resource(UserReviewsResource, '/api/user-content/<int:user_id>/reviews')
api.add_resource(UserRatingsResource, '/api/user-content/<int:user_id>/ratings')
api.add_resource(UserCommentsResource, '/api/user-content/<int:user_id>/comments')
api.add_resource(UserRecentContentResource, '/api/user-content/<int:user_id>/recent')
api.add_resource(UserTrendingContentResource, '/api/user-content/<int:user_id>/trending')
api.add_resource(UserPopularContentResource, '/api/user-content/<int:user_id>/popular')
api.add_resource(UserContentEngagementResource, '/api/user-content/<int:user_id>/content/<string:content_id>/engagement')

# Register Physics API routes
api.add_resource(PhysicsSettingsResource, '/api/physics/games/<int:universe_id>/settings')
api.add_resource(PhysicsPerformanceStatsResource, '/api/physics/games/<int:universe_id>/performance')
api.add_resource(PhysicsCollisionGroupsResource, '/api/physics/games/<int:universe_id>/collision-groups')
api.add_resource(PhysicsConstraintsResource, '/api/physics/games/<int:universe_id>/constraints')
api.add_resource(PhysicsMaterialsResource, '/api/physics/games/<int:universe_id>/materials')
api.add_resource(PhysicsPropertiesResource, '/api/physics/assets/<int:asset_id>/properties')
api.add_resource(PhysicsJointsResource, '/api/physics/games/<int:universe_id>/joints')
api.add_resource(PhysicsAssemblyResource, '/api/physics/games/<int:universe_id>/assembly')
api.add_resource(PhysicsSimulationResource, '/api/physics/games/<int:universe_id>/simulation')
api.add_resource(PhysicsRaycastResource, '/api/physics/games/<int:universe_id>/raycast')
api.add_resource(PhysicsVolumeResource, '/api/physics/games/<int:universe_id>/volumes/<int:volume_id>')
api.add_resource(PhysicsParticleEmittersResource, '/api/physics/games/<int:universe_id>/particle-emitters')
api.add_resource(PhysicsExplosionsResource, '/api/physics/games/<int:universe_id>/explosions')
api.add_resource(PhysicsForcesResource, '/api/physics/games/<int:universe_id>/forces')

# Register Education API routes
api.add_resource(EducationProviderResource, '/api/education/providers')
api.add_resource(EducationProviderDetailsResource, '/api/education/providers/<int:provider_id>')
api.add_resource(EducationCurriculumResource, '/api/education/providers/<int:provider_id>/curriculum')
api.add_resource(EducationCourseResource, '/api/education/courses/<int:course_id>')
api.add_resource(EducationLessonResource, '/api/education/lessons/<int:lesson_id>')
api.add_resource(EducationProgressResource, '/api/education/users/<int:user_id>/progress')
api.add_resource(EducationAssignmentResource, '/api/education/classes/<int:class_id>/assignments')
api.add_resource(EducationAssignmentDetailsResource, '/api/education/assignments/<int:assignment_id>')
api.add_resource(EducationClassResource, '/api/education/classes/<int:class_id>')
api.add_resource(EducationClassRosterResource, '/api/education/classes/<int:class_id>/roster')
api.add_resource(EducationEnrollmentResource, '/api/education/users/<int:user_id>/enrollments')
api.add_resource(EducationCertificateResource, '/api/education/users/<int:user_id>/certificates')
api.add_resource(EducationCertificateDetailsResource, '/api/education/certificates/<int:certificate_id>')
api.add_resource(EducationProjectResource, '/api/education/users/<int:user_id>/projects')
api.add_resource(EducationProjectDetailsResource, '/api/education/projects/<int:project_id>')
api.add_resource(EducationResourcesResource, '/api/education/resources')
api.add_resource(EducationResourceDetailsResource, '/api/education/resources/<int:resource_id>')
api.add_resource(EducationStandardsResource, '/api/education/standards')
api.add_resource(EducationStandardDetailsResource, '/api/education/standards/<int:standard_id>')

# Register Metaverse API routes
api.add_resource(MetaverseEnvironmentsResource, '/api/metaverse/environments')
api.add_resource(MetaverseEnvironmentDetailsResource, '/api/metaverse/environments/<int:environment_id>')
api.add_resource(MetaversePortalsResource, '/api/metaverse/portals')
api.add_resource(MetaversePortalDetailsResource, '/api/metaverse/portals/<int:portal_id>')
api.add_resource(MetaverseAvatarsResource, '/api/metaverse/avatars')
api.add_resource(MetaverseAvatarDetailsResource, '/api/metaverse/avatars/<int:avatar_id>')
api.add_resource(MetaverseObjectsResource, '/api/metaverse/objects')
api.add_resource(MetaverseObjectDetailsResource, '/api/metaverse/objects/<int:object_id>')
api.add_resource(MetaverseEventsResource, '/api/metaverse/events')
api.add_resource(MetaverseEventDetailsResource, '/api/metaverse/events/<int:event_id>')
api.add_resource(MetaverseEnvironmentStateResource, '/api/metaverse/environments/<int:environment_id>/state')
api.add_resource(MetaverseInteractionsResource, '/api/metaverse/environments/<int:environment_id>/interactions')
api.add_resource(MetaverseInteractionDetailsResource, '/api/metaverse/interactions/<int:interaction_id>')
api.add_resource(MetaversePerformanceResource, '/api/metaverse/environments/<int:environment_id>/performance')
api.add_resource(MetaverseUserPresenceResource, '/api/metaverse/environments/<int:environment_id>/presence')
api.add_resource(MetaverseUserPresenceHistoryResource, '/api/metaverse/users/<int:user_id>/presence-history')
api.add_resource(MetaverseMapResource, '/api/metaverse/environments/<int:environment_id>/map')
api.add_resource(MetaverseNavMeshResource, '/api/metaverse/environments/<int:environment_id>/navmesh')
api.add_resource(MetaversePathfindingResource, '/api/metaverse/environments/<int:environment_id>/pathfinding')

# Register VR/AR API routes
api.add_resource(VrCompatibleGamesResource, '/api/vr/games')
api.add_resource(VrGameDetailsResource, '/api/vr/games/<int:universe_id>')
api.add_resource(VrDeviceCompatibilityResource, '/api/vr/compatibility')
api.add_resource(VrControlsResource, '/api/vr/games/<int:universe_id>/controls')
api.add_resource(VrSettingsResource, '/api/vr/users/<int:user_id>/settings')
api.add_resource(VrPlaytimeResource, '/api/vr/users/<int:user_id>/playtime')
api.add_resource(VrPerformanceResource, '/api/vr/games/<int:universe_id>/performance')
api.add_resource(VrEventsResource, '/api/vr/events')
api.add_resource(VrEventDetailsResource, '/api/vr/events/<int:event_id>')
api.add_resource(VrTutorialsResource, '/api/vr/tutorials')
api.add_resource(VrTutorialDetailsResource, '/api/vr/tutorials/<int:tutorial_id>')
api.add_resource(ArCompatibleGamesResource, '/api/ar/games')
api.add_resource(ArGameDetailsResource, '/api/ar/games/<int:universe_id>')
api.add_resource(ArDeviceCompatibilityResource, '/api/ar/compatibility')
api.add_resource(ArControlsResource, '/api/ar/games/<int:universe_id>/controls')
api.add_resource(ArSettingsResource, '/api/ar/users/<int:user_id>/settings')
api.add_resource(ArPlaytimeResource, '/api/ar/users/<int:user_id>/playtime')

# Register Cloud API routes
api.add_resource(CloudServicesResource, '/api/cloud/services')
api.add_resource(CloudServiceDetailsResource, '/api/cloud/services/<int:service_id>')
api.add_resource(CloudStorageResource, '/api/cloud/storage')
api.add_resource(CloudStorageItemResource, '/api/cloud/storage/items/<int:item_id>')
api.add_resource(CloudDatabaseResource, '/api/cloud/databases/games/<int:universe_id>')
api.add_resource(CloudDatabaseTablesResource, '/api/cloud/databases/games/<int:universe_id>/databases/<int:database_id>/tables')
api.add_resource(CloudDatabaseTableDetailsResource, '/api/cloud/databases/games/<int:universe_id>/databases/<int:database_id>/tables/<int:table_id>')
api.add_resource(CloudFunctionsResource, '/api/cloud/functions/games/<int:universe_id>')
api.add_resource(CloudFunctionDetailsResource, '/api/cloud/functions/games/<int:universe_id>/functions/<int:function_id>')
api.add_resource(CloudFunctionLogsResource, '/api/cloud/functions/games/<int:universe_id>/functions/<int:function_id>/logs')
api.add_resource(CloudFunctionMetricsResource, '/api/cloud/functions/games/<int:universe_id>/functions/<int:function_id>/metrics')
api.add_resource(CloudMessagingResource, '/api/cloud/messaging/games/<int:universe_id>')
api.add_resource(CloudMessagingTopicsResource, '/api/cloud/messaging/games/<int:universe_id>/topics')
api.add_resource(CloudMessagingTopicDetailsResource, '/api/cloud/messaging/games/<int:universe_id>/topics/<int:topic_id>')
api.add_resource(CloudMessagingSubscriptionsResource, '/api/cloud/messaging/games/<int:universe_id>/subscriptions')
api.add_resource(CloudMessagingSubscriptionDetailsResource, '/api/cloud/messaging/games/<int:universe_id>/subscriptions/<int:subscription_id>')
api.add_resource(CloudAnalyticsResource, '/api/cloud/analytics/games/<int:universe_id>')
api.add_resource(CloudAnalyticsEventTypesResource, '/api/cloud/analytics/games/<int:universe_id>/event-types')
api.add_resource(CloudAnalyticsEventDetailsResource, '/api/cloud/analytics/games/<int:universe_id>/events/<string:event_type>')

# Register UGC API routes
api.add_resource(UgcCreatorsResource, '/api/ugc/creators')
api.add_resource(UgcCreatorDetailsResource, '/api/ugc/creators/<int:creator_id>')
api.add_resource(UgcCreatorItemsResource, '/api/ugc/creators/<int:creator_id>/items')
api.add_resource(UgcCreatorStatsResource, '/api/ugc/creators/<int:creator_id>/stats')
api.add_resource(UgcItemsResource, '/api/ugc/items')
api.add_resource(UgcItemDetailsResource, '/api/ugc/items/<int:item_id>')
api.add_resource(UgcItemStatsResource, '/api/ugc/items/<int:item_id>/stats')
api.add_resource(UgcItemReviewsResource, '/api/ugc/items/<int:item_id>/reviews')
api.add_resource(UgcItemCommentsResource, '/api/ugc/items/<int:item_id>/comments')
api.add_resource(UgcItemSalesResource, '/api/ugc/items/<int:item_id>/sales')
api.add_resource(UgcItemOwnersResource, '/api/ugc/items/<int:item_id>/owners')
api.add_resource(UgcItemSimilarResource, '/api/ugc/items/<int:item_id>/similar')
api.add_resource(UgcItemFavoritesResource, '/api/ugc/items/<int:item_id>/favorites')
api.add_resource(UgcItemVersionsResource, '/api/ugc/items/<int:item_id>/versions')
api.add_resource(UgcItemVersionDetailsResource, '/api/ugc/items/<int:item_id>/versions/<int:version_id>')
api.add_resource(UgcCategoriesResource, '/api/ugc/categories')
api.add_resource(UgcCategoryDetailsResource, '/api/ugc/categories/<int:category_id>')
api.add_resource(UgcTrendingItemsResource, '/api/ugc/trending')

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
