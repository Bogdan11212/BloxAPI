"""
Roblox API Extra Functions Wrapper

This module imports and exports all functions from the functions_extra module
to provide a uniform interface for the extended Roblox API functionality.
"""

from .functions_extra import (
    # Events API Functions
    get_user_events,
    get_game_events,
    get_group_events,
    get_event_history,
    get_event_details,
    filter_events_by_type,
    
    # Moderation API Functions
    get_content_moderation_status,
    get_moderation_history,
    check_asset_moderation,
    check_text_moderation,
    check_image_moderation,
    report_abuse,
    get_safety_settings,
    
    # Monetization API Functions
    get_developer_products,
    get_developer_product_details,
    get_game_passes,
    get_game_pass_details,
    get_premium_payouts,
    get_transaction_history,
    get_sales_summary,
    get_revenue_summary,
    get_purchases_by_product,
    check_player_ownership,
    
    # Social API Functions
    get_social_connections,
    get_social_links,
    get_followers,
    get_followings,
    get_subscribers,
    get_subscriptions,
    check_follower_status,
    check_following_status,
    get_friend_recommendations,
    get_social_graph,
    check_account_relationship,
    
    # Statistics API Functions
    get_game_universe_stats,
    get_game_version_history_stats,
    get_game_playtime_stats,
    get_game_retention_stats,
    get_game_performance_stats,
    get_game_device_stats,
    get_game_demographic_stats,
    get_game_geographic_stats,
    get_game_conversion_stats,
    get_player_activity_stats,
    get_trending_games,
    get_comparison_stats,
    
    # Servers API Functions
    get_game_server_instances,
    get_server_details,
    get_server_players,
    get_server_stats,
    get_server_logs,
    send_server_message,
    shutdown_server,
    get_server_join_script,
    get_vip_servers,
    create_vip_server,
    update_vip_server,
    get_vip_server_subscribers,
    get_private_servers,
    
    # Subscriptions API Functions
    get_user_subscriptions,
    get_user_subscribers,
    get_user_subscription_details,
    get_subscription_options,
    check_subscription_status,
    get_subscription_notifications,
    get_subscription_feed,
    
    # User Profiles API Functions
    get_user_status,
    get_user_biography,
    get_user_display_name,
    get_user_premium_status,
    get_user_presence,
    get_user_online_status,
    get_user_badges,
    get_user_membership_type,
    get_user_previous_usernames,
    get_user_age,
    get_user_join_date,
    get_user_display_name_history,
    search_users_by_display_name,
    get_user_connections,
    get_user_profile_theme,
    get_user_roblox_badges
)

# Also export RobloxAPIError for consistent error handling
from .functions_extra import RobloxAPIError