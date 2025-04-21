import json
import logging
from flask import jsonify

logger = logging.getLogger(__name__)

def format_response(data, success=True, status_code=200):
    """
    Format API response with consistent structure
    
    Args:
        data (dict): Response data
        success (bool, optional): Whether the request was successful. Defaults to True.
        status_code (int, optional): HTTP status code. Defaults to 200.
    
    Returns:
        flask.Response: Formatted JSON response with appropriate status code
    """
    response = {
        'success': success,
        'data': data
    }
    
    if not success and 'error' not in data and 'message' in data:
        # If this is an error response without an error object, reshape it
        response['data'] = {
            'error': {
                'message': data['message'],
                'code': status_code
            }
        }
    
    return jsonify(response), status_code


def format_error(message, error_code=400, error_details=None):
    """
    Format error response
    
    Args:
        message (str): Error message
        error_code (int, optional): HTTP status code. Defaults to 400.
        error_details (dict, optional): Additional error details. Defaults to None.
    
    Returns:
        flask.Response: Formatted JSON error response with appropriate status code
    """
    error = {
        'message': message,
        'code': error_code
    }
    
    if error_details:
        error['details'] = error_details
    
    return format_response({'error': error}, success=False, status_code=error_code)


def parse_api_response(response, default_error="Failed to fetch data from API"):
    """
    Parse API response and handle errors
    
    Args:
        response (requests.Response): Response from API
        default_error (str, optional): Default error message. Defaults to "Failed to fetch data from API".
    
    Returns:
        dict: Parsed response data or error object
    """
    try:
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON response from API: {response.text[:200]}")
        return {'message': "API returned invalid JSON response"}
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return {'message': default_error}