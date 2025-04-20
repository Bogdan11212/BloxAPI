from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
import logging
from utils.validators import GroupMembersSchema, PaginationSchema
from utils.roblox_api import (
    get_group_info, get_group_members,
    get_group_roles, get_user_groups,
    get_group_payouts, get_group_audit_log,
    get_group_socials, RobloxAPIError
)

logger = logging.getLogger(__name__)

class GroupResource(Resource):
    """
    Resource for getting information about a specific Roblox group
    """
    def get(self, group_id):
        """
        Get information about a group by its ID
        
        Args:
            group_id (int): The Roblox group ID
            
        Returns:
            dict: Group information or error response
        """
        try:
            group_data = get_group_info(group_id)
            
            # Check if should include user groups
            user_id = request.args.get('user_id')
            if user_id:
                try:
                    user_groups = get_user_groups(user_id)
                    group_data["userGroups"] = user_groups
                except RobloxAPIError as e:
                    logger.warning(f"Failed to get user groups: {str(e)}")
                    group_data["userGroups"] = {"error": str(e)}
            
            return {
                "success": True,
                "data": group_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting group info: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in GroupResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class GroupMembersResource(Resource):
    """
    Resource for getting members of a specific Roblox group
    """
    def get(self, group_id):
        """
        Get members of a group
        
        Args:
            group_id (int): The Roblox group ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 10)
            cursor (str, optional): Pagination cursor
            sort_order (str, optional): Sort order (Asc/Desc)
            role_id (int, optional): Filter by role ID
            
        Returns:
            dict: Group members or error response
        """
        try:
            # Validate query parameters
            schema = GroupMembersSchema()
            params = schema.load(request.args)
            
            # Get group members
            members_data = get_group_members(
                group_id, 
                params.get("limit", 10)
            )
            
            return {
                "success": True,
                "data": members_data
            }
        except ValidationError as e:
            return {
                "success": False,
                "error": {
                    "code": 400,
                    "message": "Validation error",
                    "details": e.messages
                }
            }, 400
        except RobloxAPIError as e:
            logger.error(f"Error getting group members: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in GroupMembersResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class GroupRolesResource(Resource):
    """
    Resource for getting roles of a specific Roblox group
    """
    def get(self, group_id):
        """
        Get roles of a group
        
        Args:
            group_id (int): The Roblox group ID
            
        Returns:
            dict: Group roles or error response
        """
        try:
            roles_data = get_group_roles(group_id)
            
            return {
                "success": True,
                "data": roles_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting group roles: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in GroupRolesResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class GroupPayoutsResource(Resource):
    """
    Resource for getting configured group payouts
    """
    def get(self, group_id):
        """
        Get configured group payouts
        
        Args:
            group_id (int): The Roblox group ID
            
        Returns:
            dict: Group payouts or error response
        """
        try:
            payouts_data = get_group_payouts(group_id)
            
            return {
                "success": True,
                "data": payouts_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting group payouts: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in GroupPayoutsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class GroupAuditLogResource(Resource):
    """
    Resource for getting group audit log entries
    """
    def get(self, group_id):
        """
        Get group audit log entries
        
        Args:
            group_id (int): The Roblox group ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            
        Returns:
            dict: Group audit log or error response
        """
        try:
            # Validate query parameters
            schema = PaginationSchema()
            params = schema.load(request.args)
            
            limit = params.get('limit', 50)
            
            # Get group audit log
            audit_log_data = get_group_audit_log(group_id, limit)
            
            return {
                "success": True,
                "data": audit_log_data
            }
        except ValidationError as e:
            return {
                "success": False,
                "error": {
                    "code": 400,
                    "message": "Validation error",
                    "details": e.messages
                }
            }, 400
        except RobloxAPIError as e:
            logger.error(f"Error getting group audit log: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in GroupAuditLogResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class GroupSocialsResource(Resource):
    """
    Resource for getting group social media links
    """
    def get(self, group_id):
        """
        Get group social media links
        
        Args:
            group_id (int): The Roblox group ID
            
        Returns:
            dict: Group social media links or error response
        """
        try:
            socials_data = get_group_socials(group_id)
            
            return {
                "success": True,
                "data": socials_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting group socials: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in GroupSocialsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500
