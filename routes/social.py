from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api_extra import (
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
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class SocialConnectionsResource(Resource):
    """
    Resource for getting social connections for a user
    """
    def get(self, user_id):
        """
        Get social connections for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's social connections or error response
        """
        try:
            connections_data = get_social_connections(user_id)
            
            return {
                "success": True,
                "data": connections_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting social connections: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting social connections: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SocialLinksResource(Resource):
    """
    Resource for getting social links for a user
    """
    def get(self, user_id):
        """
        Get social links for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's social links or error response
        """
        try:
            links_data = get_social_links(user_id)
            
            return {
                "success": True,
                "data": links_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting social links: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting social links: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class FollowersResource(Resource):
    """
    Resource for getting followers of a user
    """
    def get(self, user_id):
        """
        Get followers of a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: User's followers or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        cursor = request.args.get('cursor', None)
        
        try:
            followers_data = get_followers(user_id, limit, cursor)
            
            return {
                "success": True,
                "data": followers_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting followers: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting followers: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class FollowingsResource(Resource):
    """
    Resource for getting users that a user is following
    """
    def get(self, user_id):
        """
        Get users that a user is following
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: User's followings or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        cursor = request.args.get('cursor', None)
        
        try:
            followings_data = get_followings(user_id, limit, cursor)
            
            return {
                "success": True,
                "data": followings_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting followings: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting followings: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SubscribersResource(Resource):
    """
    Resource for getting subscribers of a user
    """
    def get(self, user_id):
        """
        Get subscribers of a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: User's subscribers or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        cursor = request.args.get('cursor', None)
        
        try:
            subscribers_data = get_subscribers(user_id, limit, cursor)
            
            return {
                "success": True,
                "data": subscribers_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting subscribers: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting subscribers: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SubscriptionsResource(Resource):
    """
    Resource for getting user's subscriptions
    """
    def get(self, user_id):
        """
        Get user's subscriptions
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: User's subscriptions or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        cursor = request.args.get('cursor', None)
        
        try:
            subscriptions_data = get_subscriptions(user_id, limit, cursor)
            
            return {
                "success": True,
                "data": subscriptions_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting subscriptions: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting subscriptions: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class FollowerStatusResource(Resource):
    """
    Resource for checking follower status
    """
    def get(self, user_id, follower_id):
        """
        Check if a user is a follower of another user
        
        Args:
            user_id (int): The Roblox user ID to check against
            follower_id (int): The Roblox user ID to check if they are a follower
            
        Returns:
            dict: Follower status or error response
        """
        try:
            status_data = check_follower_status(user_id, follower_id)
            
            return {
                "success": True,
                "data": status_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error checking follower status: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error checking follower status: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class FollowingStatusResource(Resource):
    """
    Resource for checking following status
    """
    def get(self, user_id, following_id):
        """
        Check if a user is following another user
        
        Args:
            user_id (int): The Roblox user ID to check
            following_id (int): The Roblox user ID to check if they are being followed
            
        Returns:
            dict: Following status or error response
        """
        try:
            status_data = check_following_status(user_id, following_id)
            
            return {
                "success": True,
                "data": status_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error checking following status: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error checking following status: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class FriendRecommendationsResource(Resource):
    """
    Resource for getting friend recommendations
    """
    def get(self, user_id):
        """
        Get friend recommendations for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 25)
            
        Returns:
            dict: Friend recommendations or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 25)
        
        try:
            recommendations_data = get_friend_recommendations(user_id, limit)
            
            return {
                "success": True,
                "data": recommendations_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting friend recommendations: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting friend recommendations: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SocialGraphResource(Resource):
    """
    Resource for getting social graph for a user
    """
    def get(self, user_id):
        """
        Get social graph for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            depth (int, optional): Depth of the social graph to retrieve (default: 1)
            limit (int, optional): Maximum number of results per level (default: 25)
            
        Returns:
            dict: Social graph or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 25)
        depth = int(request.args.get('depth', 1))
        
        try:
            graph_data = get_social_graph(user_id, depth, limit)
            
            return {
                "success": True,
                "data": graph_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting social graph: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting social graph: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class AccountRelationshipResource(Resource):
    """
    Resource for checking relationship between accounts
    """
    def get(self, user_id, other_user_id):
        """
        Check the relationship between two accounts
        
        Args:
            user_id (int): The first Roblox user ID
            other_user_id (int): The second Roblox user ID
            
        Returns:
            dict: Account relationship or error response
        """
        try:
            relationship_data = check_account_relationship(user_id, other_user_id)
            
            return {
                "success": True,
                "data": relationship_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error checking account relationship: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error checking account relationship: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500