"""
Additional API Functions for BloxAPI

This module extends the core Roblox API functionality with additional features
and endpoints for Events, Moderation, Monetization, Social, Statistics, Servers,
Subscriptions, and User Profiles.
"""

import logging
import json
import random
from datetime import datetime, timedelta

# Custom exception for Roblox API errors
class RobloxAPIError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Roblox API Error ({status_code}): {message}")

logger = logging.getLogger(__name__)

# Demo mode - For development and testing
DEMO_MODE = False

# =================================================
# Events API Functions
# =================================================
def get_user_events(user_id, max_rows=25):
    """Get event notifications for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "previousPageCursor": None,
        "nextPageCursor": "cursor123",
        "events": [
            {
                "id": 1001,
                "type": "friendRequest",
                "created": "2025-04-19T15:30:45.123Z",
                "actor": {
                    "id": 987654321,
                    "name": "AnotherDemoUser",
                    "displayName": "Another Demo"
                },
                "data": {
                    "requestId": 54321
                }
            },
            {
                "id": 1002,
                "type": "groupInvite",
                "created": "2025-04-19T12:15:22.456Z",
                "actor": {
                    "id": 987654,
                    "name": "DemoGroup",
                    "displayName": "Demo Group"
                },
                "data": {
                    "groupId": 987654,
                    "groupName": "Demo Group"
                }
            }
        ]
    }

def get_game_events(universe_id, max_rows=25):
    """Get event notifications for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "previousPageCursor": None,
        "nextPageCursor": "cursor456",
        "events": [
            {
                "id": 2001,
                "type": "placeUpdate",
                "created": "2025-04-19T17:45:12.789Z",
                "actor": {
                    "id": 1234567,
                    "name": "RobloxDemoUser",
                    "displayName": "Demo User"
                },
                "data": {
                    "placeId": 123456789,
                    "version": "v1.2.3"
                }
            },
            {
                "id": 2002,
                "type": "newBadge",
                "created": "2025-04-18T09:22:33.456Z",
                "actor": {
                    "id": 1234567,
                    "name": "RobloxDemoUser",
                    "displayName": "Demo User"
                },
                "data": {
                    "badgeId": 12345,
                    "badgeName": "Welcome to Demo Game"
                }
            }
        ]
    }

def get_group_events(group_id, max_rows=25):
    """Get event notifications for a group"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "previousPageCursor": None,
        "nextPageCursor": "cursor789",
        "events": [
            {
                "id": 3001,
                "type": "memberJoined",
                "created": "2025-04-19T14:12:54.321Z",
                "actor": {
                    "id": 34567890,
                    "name": "DemoFriend2",
                    "displayName": "Demo Friend Two"
                },
                "data": {
                    "roleId": 123,
                    "roleName": "Member"
                }
            },
            {
                "id": 3002,
                "type": "roleChange",
                "created": "2025-04-18T11:33:45.678Z",
                "actor": {
                    "id": 1234567,
                    "name": "RobloxDemoUser",
                    "displayName": "Demo User"
                },
                "target": {
                    "id": 23456789,
                    "name": "DemoFriend1",
                    "displayName": "Demo Friend One"
                },
                "data": {
                    "oldRoleId": 123,
                    "oldRoleName": "Member",
                    "newRoleId": 234,
                    "newRoleName": "Admin"
                }
            }
        ]
    }

def get_event_history(entity_type, entity_id, max_rows=25):
    """Get event history for an entity"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "previousPageCursor": None,
        "nextPageCursor": "cursorHistory",
        "events": [
            {
                "id": 4001,
                "type": "friendAccepted",
                "created": "2025-04-15T10:22:33.456Z",
                "actor": {
                    "id": 1234567,
                    "name": "RobloxDemoUser",
                    "displayName": "Demo User"
                },
                "target": {
                    "id": 23456789,
                    "name": "DemoFriend1",
                    "displayName": "Demo Friend One"
                }
            },
            {
                "id": 4002,
                "type": "badgeAwarded",
                "created": "2025-04-10T15:45:12.789Z",
                "actor": {
                    "id": 1234567890,
                    "name": "Demo Game",
                    "displayName": "Demo Game"
                },
                "target": {
                    "id": 1234567,
                    "name": "RobloxDemoUser",
                    "displayName": "Demo User"
                },
                "data": {
                    "badgeId": 12345,
                    "badgeName": "Welcome to Demo Game"
                }
            }
        ]
    }

def get_event_details(event_id):
    """Get details about a specific event"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "id": 1001,
        "type": "friendRequest",
        "created": "2025-04-19T15:30:45.123Z",
        "actor": {
            "id": 987654321,
            "name": "AnotherDemoUser",
            "displayName": "Another Demo"
        },
        "data": {
            "requestId": 54321
        },
        "details": {
            "message": "Hi, I'd like to be friends!",
            "status": "pending"
        }
    }

def filter_events_by_type(events_data, event_types):
    """Filter events by type"""
    if not events_data or "events" not in events_data:
        return events_data
    
    filtered_events = [event for event in events_data["events"] if event.get("type") in event_types]
    events_data["events"] = filtered_events
    return events_data

# =================================================
# Moderation API Functions
# =================================================
def get_content_moderation_status(content_id, content_type):
    """Check moderation status of content"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "contentId": content_id,
        "contentType": content_type,
        "status": "Approved",
        "moderationHistory": [
            {
                "date": "2025-04-15T12:34:56.789Z",
                "status": "Approved",
                "moderatorNote": "Content meets guidelines"
            }
        ],
        "lastUpdated": "2025-04-15T12:34:56.789Z"
    }

def get_moderation_history(user_id, limit=25):
    """Get moderation history for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "moderationHistory": [
            {
                "id": 1001,
                "type": "Warning",
                "reason": "Inappropriate Language",
                "created": "2025-04-01T10:20:30.456Z",
                "expires": None,
                "status": "Resolved"
            }
        ],
        "totalPages": 1,
        "totalEntries": 1
    }

def check_asset_moderation(asset_id):
    """Check moderation status of an asset"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "assetId": asset_id,
        "status": "Approved",
        "moderationNote": "Asset meets guidelines",
        "lastUpdated": "2025-04-10T15:45:12.789Z"
    }

def check_text_moderation(text):
    """Check moderation of text content"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "filteredText": text,
        "moderationStatus": "Safe",
        "violations": []
    }

def check_image_moderation(image_url):
    """Check moderation of image content"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "imageUrl": image_url,
        "moderationStatus": "Safe",
        "violations": []
    }

def report_abuse(content_id, content_type, reason, details=""):
    """Report abuse"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "reportId": 12345,
        "status": "Submitted",
        "message": "Your report has been submitted and will be reviewed by moderators."
    }

def get_safety_settings(user_id):
    """Get safety settings for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "privacySettings": {
            "whoCanMessageMe": "Friends",
            "whoCanInviteMe": "Friends",
            "whoCanFollowMe": "Everyone",
            "whoCanSeeMyInventory": "NoOne"
        },
        "chatSettings": {
            "chatEnabled": True,
            "textFilterLevel": "Medium"
        },
        "contactSettings": {
            "phoneNumberEnabled": False,
            "emailEnabled": True
        }
    }

# =================================================
# Monetization API Functions
# =================================================
def get_developer_products(universe_id, limit=50):
    """Get developer products for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "developerProducts": [
            {
                "id": 1001,
                "name": "100 Game Coins",
                "description": "Add 100 coins to your balance",
                "price": 100,
                "iconImageAssetId": 12345
            },
            {
                "id": 1002,
                "name": "Premium Membership",
                "description": "Unlock premium features for 30 days",
                "price": 400,
                "iconImageAssetId": 23456
            }
        ],
        "total": 2
    }

def get_developer_product_details(product_id):
    """Get details about a specific developer product"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "id": 1001,
        "name": "100 Game Coins",
        "description": "Add 100 coins to your balance",
        "price": 100,
        "iconImageAssetId": 12345,
        "creator": {
            "id": 1234567,
            "name": "RobloxDemoUser",
            "type": "User"
        },
        "created": "2025-03-15T08:30:45.123Z",
        "updated": "2025-04-02T14:22:33.456Z",
        "sales": 5487
    }

def get_game_passes(universe_id, limit=50):
    """Get game passes for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "gamePasses": [
            {
                "id": 2001,
                "name": "VIP Access",
                "description": "Get exclusive access to VIP areas",
                "price": 500,
                "iconImageAssetId": 34567
            },
            {
                "id": 2002,
                "name": "Double XP",
                "description": "Earn double XP for all activities",
                "price": 250,
                "iconImageAssetId": 45678
            }
        ],
        "total": 2
    }

def get_game_pass_details(pass_id):
    """Get details about a specific game pass"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "id": 2001,
        "name": "VIP Access",
        "description": "Get exclusive access to VIP areas",
        "price": 500,
        "iconImageAssetId": 34567,
        "creator": {
            "id": 1234567,
            "name": "RobloxDemoUser",
            "type": "User"
        },
        "created": "2025-02-20T11:15:30.789Z",
        "updated": "2025-03-25T16:40:55.123Z",
        "sales": 3287
    }

def get_premium_payouts(universe_id, start_date, end_date):
    """Get premium payouts for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "payoutHistory": [
            {
                "date": "2025-04-01",
                "amount": 12500,
                "engagementScore": 78.5,
                "premiumVisits": 4587,
                "eligiblePremiumUsers": 923
            },
            {
                "date": "2025-03-01",
                "amount": 9800,
                "engagementScore": 75.2,
                "premiumVisits": 3742,
                "eligiblePremiumUsers": 856
            }
        ],
        "totalPayout": 22300
    }

def get_transaction_history(universe_id, start_date, end_date, transaction_type=None, limit=100):
    """Get transaction history for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "transactions": [
            {
                "id": "txn123456",
                "type": "DeveloperProductPurchase",
                "created": "2025-04-15T14:22:33.456Z",
                "amount": 100,
                "currency": "Robux",
                "details": {
                    "productId": 1001,
                    "productName": "100 Game Coins"
                },
                "agent": {
                    "id": 987654321,
                    "name": "AnotherDemoUser",
                    "type": "User"
                }
            },
            {
                "id": "txn123457",
                "type": "GamePassPurchase",
                "created": "2025-04-12T09:45:12.789Z",
                "amount": 500,
                "currency": "Robux",
                "details": {
                    "gamePassId": 2001,
                    "gamePassName": "VIP Access"
                },
                "agent": {
                    "id": 23456789,
                    "name": "DemoFriend1",
                    "type": "User"
                }
            }
        ],
        "total": 2,
        "nextPageCursor": None
    }

def get_sales_summary(universe_id, start_date, end_date):
    """Get sales summary for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "summary": {
            "totalSalesCount": 8772,
            "totalSalesAmount": 2574300,
            "developerProductSalesCount": 5487,
            "developerProductSalesAmount": 1236800,
            "gamePassSalesCount": 3285,
            "gamePassSalesAmount": 1337500
        },
        "products": [
            {
                "id": 1001,
                "name": "100 Game Coins",
                "salesCount": 3245,
                "salesAmount": 324500
            },
            {
                "id": 1002,
                "name": "Premium Membership",
                "salesCount": 2242,
                "salesAmount": 912300
            }
        ],
        "gamePasses": [
            {
                "id": 2001,
                "name": "VIP Access",
                "salesCount": 1856,
                "salesAmount": 928000
            },
            {
                "id": 2002,
                "name": "Double XP",
                "salesCount": 1429,
                "salesAmount": 409500
            }
        ]
    }

def get_revenue_summary(universe_id, start_date, end_date):
    """Get revenue summary for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "summary": {
            "totalRevenue": 1824510,
            "developerProductRevenue": 865760,
            "gamePassRevenue": 936250,
            "premiumPayouts": 22500
        },
        "revenueTrend": [
            {
                "date": "2025-04-01",
                "revenue": 56830,
                "developerProductRevenue": 26950,
                "gamePassRevenue": 29880
            },
            {
                "date": "2025-04-02",
                "revenue": 61250,
                "developerProductRevenue": 28700,
                "gamePassRevenue": 32550
            }
        ]
    }

def get_purchases_by_product(universe_id, product_id, start_date, end_date, limit=100):
    """Get purchases by product"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "purchases": [
            {
                "id": "prc123456",
                "created": "2025-04-15T14:22:33.456Z",
                "amount": 100,
                "currency": "Robux",
                "buyer": {
                    "id": 987654321,
                    "name": "AnotherDemoUser",
                    "type": "User"
                }
            },
            {
                "id": "prc123457",
                "created": "2025-04-14T11:15:30.789Z",
                "amount": 100,
                "currency": "Robux",
                "buyer": {
                    "id": 23456789,
                    "name": "DemoFriend1",
                    "type": "User"
                }
            }
        ],
        "total": 2,
        "nextPageCursor": None
    }

def check_player_ownership(user_id, asset_type, asset_id):
    """Check if a player owns a product"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "owns": True,
        "purchaseDate": "2025-04-10T15:45:12.789Z"
    }

# =================================================
# Social API Functions
# =================================================
def get_social_connections(user_id):
    """Get social connections for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "friends": {
            "count": 3,
            "mutualCount": 1
        },
        "followers": {
            "count": 50
        },
        "following": {
            "count": 25
        },
        "groups": {
            "count": 5
        }
    }

def get_social_links(user_id):
    """Get social links for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "links": [
            {
                "type": "Twitter",
                "url": "https://twitter.com/demolink",
                "title": "Follow me on Twitter!"
            },
            {
                "type": "YouTube",
                "url": "https://youtube.com/demolink",
                "title": "Check out my YouTube channel!"
            }
        ]
    }

def get_followers(user_id, limit=50, cursor=None):
    """Get followers of a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 23456789,
                "name": "DemoFriend1",
                "displayName": "Demo Friend One",
                "hasVerifiedBadge": False,
                "created": "2020-07-15T08:45:12.38Z"
            },
            {
                "id": 34567890,
                "name": "DemoFriend2",
                "displayName": "Demo Friend Two",
                "hasVerifiedBadge": False,
                "created": "2019-02-28T12:34:56.78Z"
            }
        ],
        "previousPageCursor": None,
        "nextPageCursor": "cursorFollowers"
    }

def get_followings(user_id, limit=50, cursor=None):
    """Get users that a user is following"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 45678901,
                "name": "DemoFriend3",
                "displayName": "Demo Friend Three",
                "hasVerifiedBadge": True,
                "created": "2021-04-12T18:22:47.15Z"
            }
        ],
        "previousPageCursor": None,
        "nextPageCursor": None
    }

def get_subscribers(user_id, limit=50, cursor=None):
    """Get subscribers of a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 56789012,
                "name": "DemoSubscriber1",
                "displayName": "Demo Subscriber One",
                "hasVerifiedBadge": False,
                "created": "2022-05-15T08:45:12.38Z",
                "subscriptionDate": "2025-01-15T14:22:33.456Z"
            }
        ],
        "previousPageCursor": None,
        "nextPageCursor": None
    }

def get_subscriptions(user_id, limit=50, cursor=None):
    """Get user's subscriptions"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 67890123,
                "name": "DemoCreator1",
                "displayName": "Demo Creator One",
                "hasVerifiedBadge": True,
                "created": "2018-08-22T11:15:30.789Z",
                "subscriptionDate": "2025-02-20T09:45:12.789Z"
            }
        ],
        "previousPageCursor": None,
        "nextPageCursor": None
    }

def check_follower_status(user_id, follower_id):
    """Check if a user is a follower of another user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "isFollowing": True,
        "followingDate": "2025-03-15T08:30:45.123Z"
    }

def check_following_status(user_id, following_id):
    """Check if a user is following another user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "isFollowing": True,
        "followingDate": "2025-03-15T08:30:45.123Z"
    }

def get_friend_recommendations(user_id, limit=25):
    """Get friend recommendations for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 78901234,
                "name": "DemoRecommendation1",
                "displayName": "Demo Recommendation One",
                "hasVerifiedBadge": False,
                "mutualFriendsCount": 2,
                "mutualFriends": [
                    {
                        "id": 23456789,
                        "name": "DemoFriend1"
                    },
                    {
                        "id": 34567890,
                        "name": "DemoFriend2"
                    }
                ]
            }
        ]
    }

def get_social_graph(user_id, depth=1, limit=25):
    """Get social graph for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "rootUser": {
            "id": 1234567,
            "name": "RobloxDemoUser",
            "displayName": "Demo User"
        },
        "friends": [
            {
                "id": 23456789,
                "name": "DemoFriend1",
                "displayName": "Demo Friend One",
                "friends": [] if depth < 2 else [
                    {
                        "id": 78901234,
                        "name": "DemoRecommendation1",
                        "displayName": "Demo Recommendation One"
                    }
                ]
            },
            {
                "id": 34567890,
                "name": "DemoFriend2",
                "displayName": "Demo Friend Two",
                "friends": [] if depth < 2 else [
                    {
                        "id": 78901234,
                        "name": "DemoRecommendation1",
                        "displayName": "Demo Recommendation One"
                    }
                ]
            }
        ]
    }

def check_account_relationship(user_id, other_user_id):
    """Check relationship between accounts"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "areFriends": True,
        "friendshipStatus": "Friends",
        "friendshipCreated": "2025-01-15T14:22:33.456Z",
        "isFollowing": True,
        "followingDate": "2024-12-10T09:45:12.789Z",
        "isFollowedBy": True,
        "followedByDate": "2024-12-12T11:15:30.789Z",
        "canMessage": True,
        "areMutualFriends": False,
        "mutualFriendsCount": 0
    }

# =================================================
# Statistics API Functions
# =================================================
def get_game_universe_stats(universe_id, start_date, end_date):
    """Get universe statistics for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "placeVisits": 5248679,
        "totalPlayers": 1789542,
        "averagePlaytime": 1250,  # in seconds
        "averageDailyActiveUsers": 45678,
        "concurrentPeaks": [
            {
                "date": "2025-04-15",
                "count": 5678
            },
            {
                "date": "2025-04-16",
                "count": 6123
            }
        ],
        "visitsHistory": [
            {
                "date": "2025-04-15",
                "count": 128456
            },
            {
                "date": "2025-04-16",
                "count": 135789
            }
        ]
    }

def get_game_version_history_stats(universe_id, limit=50):
    """Get version history statistics for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "versions": [
            {
                "version": "v1.2.3",
                "publishedDate": "2025-04-10T14:22:33.456Z",
                "visits": 458123,
                "averagePlaytime": 1340,  # in seconds
                "performance": {
                    "averageFps": 58.7,
                    "averageMemoryUsage": 2456  # in MB
                }
            },
            {
                "version": "v1.2.2",
                "publishedDate": "2025-03-25T11:15:30.789Z",
                "visits": 789456,
                "averagePlaytime": 1220,  # in seconds
                "performance": {
                    "averageFps": 57.2,
                    "averageMemoryUsage": 2498  # in MB
                }
            }
        ],
        "total": 2
    }

def get_game_playtime_stats(universe_id, start_date, end_date):
    """Get playtime statistics for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "totalPlaytime": 2145876950,  # in seconds
        "averagePlaytime": 1250,  # in seconds
        "playtimeDistribution": {
            "lessThan5Minutes": 0.25,
            "5to15Minutes": 0.35,
            "15to30Minutes": 0.20,
            "30to60Minutes": 0.15,
            "moreThan60Minutes": 0.05
        },
        "dailyPlaytime": [
            {
                "date": "2025-04-15",
                "totalPlaytime": 56789210,  # in seconds
                "averagePlaytime": 1320  # in seconds
            },
            {
                "date": "2025-04-16",
                "totalPlaytime": 58123450,  # in seconds
                "averagePlaytime": 1280  # in seconds
            }
        ]
    }

def get_game_retention_stats(universe_id, start_date, end_date):
    """Get retention statistics for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "overall": {
            "day1Retention": 0.45,
            "day7Retention": 0.25,
            "day30Retention": 0.12
        },
        "cohorts": [
            {
                "date": "2025-04-10",
                "newPlayers": 12345,
                "day1Retention": 0.48,
                "day7Retention": 0.28,
                "day30Retention": None  # Not enough days passed
            },
            {
                "date": "2025-04-03",
                "newPlayers": 10987,
                "day1Retention": 0.47,
                "day7Retention": 0.26,
                "day30Retention": None  # Not enough days passed
            }
        ]
    }

def get_game_performance_stats(universe_id, start_date, end_date):
    """Get performance statistics for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "overall": {
            "averageFps": 58.2,
            "averageMemoryUsage": 2475,  # in MB
            "averageLoadTime": 12.5,  # in seconds
            "serverCrashes": 23
        },
        "daily": [
            {
                "date": "2025-04-15",
                "averageFps": 58.7,
                "averageMemoryUsage": 2456,  # in MB
                "averageLoadTime": 12.2,  # in seconds
                "serverCrashes": 5
            },
            {
                "date": "2025-04-16",
                "averageFps": 58.5,
                "averageMemoryUsage": 2467,  # in MB
                "averageLoadTime": 12.4,  # in seconds
                "serverCrashes": 3
            }
        ]
    }

def get_game_device_stats(universe_id, start_date, end_date):
    """Get device statistics for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "devices": {
            "Computer": 0.45,
            "Phone": 0.35,
            "Tablet": 0.15,
            "Console": 0.05
        },
        "operatingSystems": {
            "Windows": 0.40,
            "iOS": 0.30,
            "Android": 0.20,
            "MacOS": 0.05,
            "Xbox": 0.03,
            "PlayStation": 0.02
        },
        "daily": [
            {
                "date": "2025-04-15",
                "devices": {
                    "Computer": 0.44,
                    "Phone": 0.36,
                    "Tablet": 0.15,
                    "Console": 0.05
                }
            },
            {
                "date": "2025-04-16",
                "devices": {
                    "Computer": 0.45,
                    "Phone": 0.35,
                    "Tablet": 0.15,
                    "Console": 0.05
                }
            }
        ]
    }

def get_game_demographic_stats(universe_id, start_date, end_date):
    """Get demographic statistics for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "demographics": {
            "ageRanges": {
                "under13": 0.35,
                "13to17": 0.40,
                "18to24": 0.15,
                "25andOver": 0.10
            },
            "gender": {
                "male": 0.55,
                "female": 0.45
            }
        }
    }

def get_game_geographic_stats(universe_id, start_date, end_date):
    """Get geographic statistics for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "countries": {
            "US": 0.35,
            "UK": 0.15,
            "CA": 0.10,
            "AU": 0.08,
            "BR": 0.05,
            "Other": 0.27
        },
        "languages": {
            "English": 0.60,
            "Spanish": 0.15,
            "Portuguese": 0.08,
            "French": 0.05,
            "Other": 0.12
        }
    }

def get_game_conversion_stats(universe_id, start_date, end_date):
    """Get conversion statistics for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "conversions": {
            "gamePassConversion": 0.15,
            "developerProductConversion": 0.22,
            "overallConversion": 0.30
        },
        "topConvertingItems": [
            {
                "id": 2001,
                "name": "VIP Access",
                "type": "GamePass",
                "conversionRate": 0.08
            },
            {
                "id": 1001,
                "name": "100 Game Coins",
                "type": "DeveloperProduct",
                "conversionRate": 0.12
            }
        ]
    }

def get_player_activity_stats(user_id, start_date, end_date):
    """Get activity statistics for a player"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "totalPlaytime": 45678,  # in minutes
        "gamesPlayed": 28,
        "visitedGames": [
            {
                "universeId": 4567890123,
                "name": "Demo Game",
                "visits": 45,
                "playtime": 1890  # in minutes
            },
            {
                "universeId": 9876543210,
                "name": "Another Demo Game",
                "visits": 32,
                "playtime": 1240  # in minutes
            }
        ],
        "playByDay": [
            {
                "date": "2025-04-15",
                "playtime": 120,  # in minutes
                "gamesPlayed": 3
            },
            {
                "date": "2025-04-16",
                "playtime": 150,  # in minutes
                "gamesPlayed": 4
            }
        ]
    }

def get_trending_games(limit=50, genre=None, age_group=None, time_frame="day"):
    """Get trending games"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "games": [
            {
                "universeId": 4567890123,
                "name": "Demo Game",
                "creator": {
                    "id": 1234567,
                    "name": "RobloxDemoUser",
                    "type": "User"
                },
                "playerCount": 1254,
                "visits": 5248679,
                "thumbnail": "https://example.com/thumbnail1.jpg",
                "rankChange": 2
            },
            {
                "universeId": 9876543210,
                "name": "Another Demo Game",
                "creator": {
                    "id": 987654321,
                    "name": "AnotherDemoUser",
                    "type": "User"
                },
                "playerCount": 847,
                "visits": 1389452,
                "thumbnail": "https://example.com/thumbnail2.jpg",
                "rankChange": -1
            }
        ]
    }

def get_comparison_stats(universe_ids, metric, start_date, end_date):
    """Get comparison statistics for games"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "metric": metric,
        "startDate": start_date,
        "endDate": end_date,
        "universes": [
            {
                "universeId": 4567890123,
                "name": "Demo Game",
                "value": metric == "visits" and 5248679 or (metric == "revenue" and 285674 or 1250)
            },
            {
                "universeId": 9876543210,
                "name": "Another Demo Game",
                "value": metric == "visits" and 1389452 or (metric == "revenue" and 125896 or 980)
            }
        ],
        "dailyData": [
            {
                "date": "2025-04-15",
                "values": {
                    "4567890123": metric == "visits" and 128456 or (metric == "revenue" and 7845 or 1320),
                    "9876543210": metric == "visits" and 45678 or (metric == "revenue" and 3254 or 950)
                }
            },
            {
                "date": "2025-04-16",
                "values": {
                    "4567890123": metric == "visits" and 135789 or (metric == "revenue" and 8123 or 1280),
                    "9876543210": metric == "visits" and 48123 or (metric == "revenue" and 3456 or 990)
                }
            }
        ]
    }

# =================================================
# Servers API Functions
# =================================================
def get_game_server_instances(universe_id, limit=25, cursor=None, min_players=None, max_players=None, exclude_full=False):
    """Get server instances for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": "01f5b791-e67f-156d-a82c-49c882b22313",
                "maxPlayers": 50,
                "playing": 32,
                "playerTokens": ["Player1", "Player2"],
                "fps": 57.8,
                "ping": 45.2,
                "name": "Main Server 1",
                "vip": False
            },
            {
                "id": "02g6c892-f78g-267e-b93d-59c983c33424",
                "maxPlayers": 50,
                "playing": 45,
                "playerTokens": ["Player3", "Player4"],
                "fps": 58.2,
                "ping": 42.5,
                "name": "Main Server 2",
                "vip": False
            }
        ],
        "nextPageCursor": "serverCursor123"
    }

def get_server_details(server_id):
    """Get details about a server"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "id": "01f5b791-e67f-156d-a82c-49c882b22313",
        "maxPlayers": 50,
        "playing": 32,
        "fps": 57.8,
        "ping": 45.2,
        "name": "Main Server 1",
        "vip": False,
        "placeId": 123456789,
        "universeId": 4567890123,
        "region": "US-East",
        "uptime": 12543,  # in seconds
        "status": "Running"
    }

def get_server_players(server_id):
    """Get players in a server"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 987654321,
                "name": "AnotherDemoUser",
                "displayName": "Another Demo"
            },
            {
                "id": 23456789,
                "name": "DemoFriend1",
                "displayName": "Demo Friend One"
            }
        ],
        "total": 2
    }

def get_server_stats(server_id):
    """Get stats about a server"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "fps": 57.8,
        "ping": 45.2,
        "memory": 2456,  # in MB
        "uptime": 12543,  # in seconds
        "players": 32,
        "maxPlayers": 50
    }

def get_server_logs(server_id, limit=100):
    """Get logs from a server"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "timestamp": "2025-04-20T14:22:33.456Z",
                "level": "INFO",
                "message": "Player AnotherDemoUser joined the game"
            },
            {
                "timestamp": "2025-04-20T14:25:45.789Z",
                "level": "INFO",
                "message": "Player DemoFriend1 joined the game"
            }
        ],
        "nextPageCursor": None
    }

def send_server_message(server_id, message):
    """Send a message to a server"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "success": True,
        "message": "Message sent successfully"
    }

def shutdown_server(server_id):
    """Shut down a server"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "success": True,
        "message": "Server shutdown initiated"
    }

def get_server_join_script(server_id):
    """Get the join script for a server"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "joinScript": "-- This would be an actual join script in real API"
    }

def get_vip_servers(universe_id, limit=25, cursor=None):
    """Get VIP servers for a game"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": "vip-01f5b791-e67f-156d-a82c-49c882b22313",
                "name": "My VIP Server",
                "maxPlayers": 50,
                "playing": 5,
                "owner": {
                    "id": 1234567,
                    "name": "RobloxDemoUser",
                    "type": "User"
                },
                "price": 100,
                "active": True,
                "joinCode": "ABC123"
            }
        ],
        "nextPageCursor": None
    }

def create_vip_server(universe_id, name, price=None):
    """Create a VIP server"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "id": "vip-01f5b791-e67f-156d-a82c-49c882b22313",
        "name": name,
        "maxPlayers": 50,
        "playing": 0,
        "owner": {
            "id": 1234567,
            "name": "RobloxDemoUser",
            "type": "User"
        },
        "price": price or 100,
        "active": True,
        "joinCode": "ABC123"
    }

def update_vip_server(server_id, data):
    """Update a VIP server"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "id": server_id,
        "name": data.get("name", "My VIP Server"),
        "maxPlayers": 50,
        "playing": 5,
        "owner": {
            "id": 1234567,
            "name": "RobloxDemoUser",
            "type": "User"
        },
        "price": 100,
        "active": data.get("active", True),
        "joinCode": data.get("joinCode", "ABC123")
    }

def get_vip_server_subscribers(server_id, limit=25, cursor=None):
    """Get subscribers to a VIP server"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 987654321,
                "name": "AnotherDemoUser",
                "displayName": "Another Demo",
                "hasVerifiedBadge": False
            },
            {
                "id": 23456789,
                "name": "DemoFriend1",
                "displayName": "Demo Friend One",
                "hasVerifiedBadge": False
            }
        ],
        "nextPageCursor": None
    }

def get_private_servers(user_id, limit=25, cursor=None):
    """Get private servers for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": "vip-01f5b791-e67f-156d-a82c-49c882b22313",
                "name": "My VIP Server",
                "game": {
                    "id": 4567890123,
                    "name": "Demo Game"
                },
                "maxPlayers": 50,
                "playing": 5,
                "active": True,
                "joinCode": "ABC123"
            }
        ],
        "nextPageCursor": None
    }

# =================================================
# Subscriptions API Functions
# =================================================
def get_user_subscriptions(user_id, limit=50, cursor=None):
    """Get subscriptions for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 1001,
                "target": {
                    "id": 67890123,
                    "name": "DemoCreator1",
                    "type": "User"
                },
                "created": "2025-02-20T09:45:12.789Z",
                "expires": "2026-02-20T09:45:12.789Z",
                "status": "Active"
            }
        ],
        "nextPageCursor": None
    }

def get_user_subscribers(user_id, limit=50, cursor=None):
    """Get subscribers for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 2001,
                "subscriber": {
                    "id": 56789012,
                    "name": "DemoSubscriber1",
                    "type": "User"
                },
                "created": "2025-01-15T14:22:33.456Z",
                "expires": "2026-01-15T14:22:33.456Z",
                "status": "Active"
            }
        ],
        "nextPageCursor": None
    }

def get_user_subscription_details(user_id, subscription_id):
    """Get details about a user's subscription"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "id": 1001,
        "target": {
            "id": 67890123,
            "name": "DemoCreator1",
            "type": "User"
        },
        "created": "2025-02-20T09:45:12.789Z",
        "expires": "2026-02-20T09:45:12.789Z",
        "status": "Active",
        "price": 499,
        "renewalPeriod": "Monthly",
        "autoRenewEnabled": True,
        "benefits": [
            "Exclusive Content",
            "Special Badge",
            "Early Access"
        ]
    }

def get_subscription_options(entity_type, entity_id):
    """Get subscription options for a user or entity"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "options": [
            {
                "id": 1001,
                "name": "Standard",
                "price": 499,
                "period": "Monthly",
                "benefits": [
                    "Exclusive Content",
                    "Special Badge"
                ]
            },
            {
                "id": 1002,
                "name": "Premium",
                "price": 999,
                "period": "Monthly",
                "benefits": [
                    "Exclusive Content",
                    "Special Badge",
                    "Early Access",
                    "VIP Support"
                ]
            }
        ]
    }

def check_subscription_status(user_id, entity_type, entity_id):
    """Check subscription status"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "isSubscribed": True,
        "subscriptionId": 1001,
        "tier": "Standard",
        "created": "2025-02-20T09:45:12.789Z",
        "expires": "2026-02-20T09:45:12.789Z",
        "autoRenewEnabled": True
    }

def get_subscription_notifications(user_id, limit=50, cursor=None):
    """Get subscription notifications for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 3001,
                "type": "ContentRelease",
                "created": "2025-04-15T14:22:33.456Z",
                "subscription": {
                    "id": 1001,
                    "target": {
                        "id": 67890123,
                        "name": "DemoCreator1",
                        "type": "User"
                    }
                },
                "content": {
                    "title": "New Exclusive Content",
                    "description": "Check out our new exclusive content!"
                }
            }
        ],
        "nextPageCursor": None
    }

def get_subscription_feed(user_id, limit=50, cursor=None):
    """Get subscription feed for a user"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 4001,
                "type": "Post",
                "created": "2025-04-15T14:22:33.456Z",
                "author": {
                    "id": 67890123,
                    "name": "DemoCreator1",
                    "type": "User"
                },
                "content": {
                    "title": "New Update Coming Soon",
                    "body": "We're excited to announce our new update coming next week!",
                    "mediaUrl": "https://example.com/media1.jpg"
                },
                "likes": 158,
                "comments": 32
            }
        ],
        "nextPageCursor": None
    }

# =================================================
# User Profiles API Functions
# =================================================
def get_user_status(user_id):
    """Get a user's status"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "status": "Working on some cool new features!"
    }

def get_user_biography(user_id):
    """Get a user's biography"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "biography": "Roblox developer who loves creating cool games and experiences."
    }

def get_user_display_name(user_id):
    """Get a user's display name"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "displayName": "Demo User"
    }

def get_user_premium_status(user_id):
    """Get a user's premium status"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "isPremium": True,
        "premiumType": "Premium1000",
        "membershipStart": "2023-01-15T14:22:33.456Z"
    }

def get_user_presence(user_id):
    """Get a user's presence information"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "userPresenceType": 1,  # 1 = Online, 2 = In Game, 3 = Offline
        "lastOnline": "2025-04-20T12:35:46.789Z",
        "placeId": 8579496407,
        "rootPlaceId": 8579496407,
        "gameId": "01f5b791-e67f-156d-a82c-49c882b22313",
        "universeId": 3254815126,
        "lastLocation": "Brookhaven RP"
    }

def get_user_online_status(user_id):
    """Get a user's online status"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "isOnline": True,
        "lastOnline": "2025-04-20T12:35:46.789Z"
    }

def get_user_badges(user_id):
    """Get a user's profile badges"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "badges": [
            {
                "id": 12345,
                "name": "Welcome to Demo Game",
                "description": "Join the game for the first time",
                "iconImageId": 654321,
                "awardedDate": "2025-01-15T14:22:33.456Z"
            },
            {
                "id": 23456,
                "name": "Master Demo Player",
                "description": "Complete all levels in Demo Game",
                "iconImageId": 765432,
                "awardedDate": "2025-02-20T09:45:12.789Z"
            }
        ],
        "total": 2
    }

def get_user_membership_type(user_id):
    """Get a user's membership type"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "membershipType": "Premium",
        "membershipTypeId": 4,
        "isPremium": True,
        "isLifetime": False,
        "expires": "2026-01-15T14:22:33.456Z"
    }

def get_user_previous_usernames(user_id):
    """Get a user's previous usernames"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "previousUsernames": [
            "OldDemoUser",
            "RobloxDemoUser123"
        ]
    }

def get_user_age(user_id):
    """Get a user's age"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "accountAge": 1520,  # in days
        "membershipAge": 842  # in days
    }

def get_user_join_date(user_id):
    """Get a user's join date"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "joinDate": "2019-08-02T18:45:26.91Z"
    }

def get_user_display_name_history(user_id):
    """Get a user's display name history"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "displayNames": [
            {
                "name": "Demo User",
                "updated": "2024-06-15T11:22:33.456Z"
            },
            {
                "name": "RobloxUser",
                "updated": "2022-03-10T09:45:12.789Z"
            }
        ]
    }

def search_users_by_display_name(display_name, limit=50):
    """Search users by display name"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "data": [
            {
                "id": 1234567,
                "name": "RobloxDemoUser",
                "displayName": "Demo User",
                "hasVerifiedBadge": True
            },
            {
                "id": 8901234,
                "name": "AnotherDemoUser2",
                "displayName": "Demo User 2",
                "hasVerifiedBadge": False
            }
        ],
        "total": 2
    }

def get_user_connections(user_id):
    """Get a user's connections"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "connections": [
            {
                "type": "Discord",
                "name": "demo_user#1234",
                "isVerified": True,
                "isPublic": True
            },
            {
                "type": "Twitter",
                "name": "@demo_user",
                "isVerified": True,
                "isPublic": True
            }
        ]
    }

def get_user_profile_theme(user_id):
    """Get a user's profile theme"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "themeType": "Custom",
        "themeName": "Space Explorer",
        "colors": {
            "background": "#0f1729",
            "foreground": "#ffffff",
            "accent": "#6366f1"
        },
        "images": {
            "background": "https://example.com/background.jpg",
            "banner": "https://example.com/banner.jpg"
        }
    }

def get_user_roblox_badges(user_id):
    """Get a user's Roblox badges"""
    if not DEMO_MODE:
        # In a real implementation, this would call the actual Roblox API
        raise RobloxAPIError(501, "Live API not implemented")
    
    # Return demo data
    return {
        "badges": [
            {
                "id": 1,
                "name": "Administrator",
                "description": "This badge identifies an account as belonging to a Roblox administrator.",
                "imageUrl": "https://example.com/admin-badge.png"
            },
            {
                "id": 12,
                "name": "Veteran",
                "description": "This badge recognizes members who have played Roblox for at least a year.",
                "imageUrl": "https://example.com/veteran-badge.png"
            }
        ]
    }