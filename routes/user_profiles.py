from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api_extra import (
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
    get_user_roblox_badges,
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class UserStatusResource(Resource):
    """
    Resource for getting a user's status
    """
    def get(self, user_id):
        """
        Get a user's status
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's status or error response
        """
        try:
            status_data = get_user_status(user_id)
            
            return {
                "success": True,
                "data": status_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user status: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user status: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserBiographyResource(Resource):
    """
    Resource for getting a user's biography
    """
    def get(self, user_id):
        """
        Get a user's biography
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's biography or error response
        """
        try:
            bio_data = get_user_biography(user_id)
            
            return {
                "success": True,
                "data": bio_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user biography: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user biography: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserDisplayNameResource(Resource):
    """
    Resource for getting a user's display name
    """
    def get(self, user_id):
        """
        Get a user's display name
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's display name or error response
        """
        try:
            display_name_data = get_user_display_name(user_id)
            
            return {
                "success": True,
                "data": display_name_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user display name: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user display name: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserPremiumStatusResource(Resource):
    """
    Resource for getting a user's premium status
    """
    def get(self, user_id):
        """
        Get a user's premium status
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's premium status or error response
        """
        try:
            premium_data = get_user_premium_status(user_id)
            
            return {
                "success": True,
                "data": premium_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user premium status: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user premium status: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserProfilePresenceResource(Resource):
    """
    Resource for getting a user's presence
    """
    def get(self, user_id):
        """
        Get a user's presence
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's presence information or error response
        """
        try:
            presence_data = get_user_presence(user_id)
            
            return {
                "success": True,
                "data": presence_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user presence: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user presence: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserOnlineStatusResource(Resource):
    """
    Resource for getting a user's online status
    """
    def get(self, user_id):
        """
        Get a user's online status
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's online status or error response
        """
        try:
            status_data = get_user_online_status(user_id)
            
            return {
                "success": True,
                "data": status_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user online status: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user online status: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserProfileBadgesResource(Resource):
    """
    Resource for getting a user's profile badges
    """
    def get(self, user_id):
        """
        Get a user's profile badges
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's profile badges or error response
        """
        try:
            badges_data = get_user_badges(user_id)
            
            return {
                "success": True,
                "data": badges_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user badges: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user badges: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserMembershipTypeResource(Resource):
    """
    Resource for getting a user's membership type
    """
    def get(self, user_id):
        """
        Get a user's membership type
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's membership type or error response
        """
        try:
            membership_data = get_user_membership_type(user_id)
            
            return {
                "success": True,
                "data": membership_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user membership type: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user membership type: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserPreviousUsernamesResource(Resource):
    """
    Resource for getting a user's previous usernames
    """
    def get(self, user_id):
        """
        Get a user's previous usernames
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's previous usernames or error response
        """
        try:
            usernames_data = get_user_previous_usernames(user_id)
            
            return {
                "success": True,
                "data": usernames_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user previous usernames: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user previous usernames: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserAgeResource(Resource):
    """
    Resource for getting a user's age
    """
    def get(self, user_id):
        """
        Get a user's age
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's age or error response
        """
        try:
            age_data = get_user_age(user_id)
            
            return {
                "success": True,
                "data": age_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user age: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user age: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserJoinDateResource(Resource):
    """
    Resource for getting a user's join date
    """
    def get(self, user_id):
        """
        Get a user's join date
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's join date or error response
        """
        try:
            join_date_data = get_user_join_date(user_id)
            
            return {
                "success": True,
                "data": join_date_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user join date: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user join date: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserDisplayNameHistoryResource(Resource):
    """
    Resource for getting a user's display name history
    """
    def get(self, user_id):
        """
        Get a user's display name history
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's display name history or error response
        """
        try:
            history_data = get_user_display_name_history(user_id)
            
            return {
                "success": True,
                "data": history_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user display name history: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user display name history: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SearchUsersByDisplayNameResource(Resource):
    """
    Resource for searching users by display name
    """
    def get(self):
        """
        Search users by display name
        
        Query Parameters:
            display_name (str, required): The display name to search for
            limit (int, optional): Maximum number of results (default: 50)
            
        Returns:
            dict: Search results or error response
        """
        display_name = request.args.get('display_name', None)
        
        if not display_name:
            return {
                "success": False,
                "message": "Missing required parameter: display_name"
            }, 400
        
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        
        try:
            search_data = search_users_by_display_name(display_name, limit)
            
            return {
                "success": True,
                "data": search_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error searching users by display name: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error searching users by display name: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserConnectionsResource(Resource):
    """
    Resource for getting a user's connections
    """
    def get(self, user_id):
        """
        Get a user's connections
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's connections or error response
        """
        try:
            connections_data = get_user_connections(user_id)
            
            return {
                "success": True,
                "data": connections_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user connections: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user connections: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserProfileThemeResource(Resource):
    """
    Resource for getting a user's profile theme
    """
    def get(self, user_id):
        """
        Get a user's profile theme
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's profile theme or error response
        """
        try:
            theme_data = get_user_profile_theme(user_id)
            
            return {
                "success": True,
                "data": theme_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user profile theme: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user profile theme: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserRobloxBadgesResource(Resource):
    """
    Resource for getting a user's Roblox badges
    """
    def get(self, user_id):
        """
        Get a user's Roblox badges
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's Roblox badges or error response
        """
        try:
            badges_data = get_user_roblox_badges(user_id)
            
            return {
                "success": True,
                "data": badges_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user Roblox badges: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user Roblox badges: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500