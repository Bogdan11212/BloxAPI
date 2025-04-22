"""
GraphQL Route for BloxAPI

This module provides a GraphQL API endpoint for more flexible querying
of the BloxAPI data.
"""

import logging
import json
from flask import request, jsonify
from flask_restful import Resource
from utils.graphql_schema import schema

# Configure logging
logger = logging.getLogger(__name__)

class GraphQLResource(Resource):
    """
    Resource for GraphQL API
    """
    
    def get(self):
        """
        Handle GET requests to the GraphQL endpoint
        
        Returns:
            GraphQL query results or error response
        """
        try:
            # Parse query from GET parameters
            query = request.args.get('query')
            variables = request.args.get('variables')
            
            if variables:
                try:
                    variables = json.loads(variables)
                except json.JSONDecodeError:
                    return {"error": "Invalid variables JSON"}, 400
            
            if not query:
                return {"error": "No GraphQL query provided"}, 400
            
            # Execute query
            result = schema.execute(query, variable_values=variables)
            
            if result.errors:
                # Log errors
                for error in result.errors:
                    logger.error(f"GraphQL error: {error}")
                
                # Return errors
                errors = [str(error) for error in result.errors]
                return {"errors": errors}, 400
            
            # Return data
            return jsonify(result.data)
        
        except Exception as e:
            logger.error(f"Error processing GraphQL query: {e}")
            return {"error": str(e)}, 500
    
    def post(self):
        """
        Handle POST requests to the GraphQL endpoint
        
        Returns:
            GraphQL query results or error response
        """
        try:
            # Parse JSON data from request
            data = request.get_json()
            
            if not data:
                return {"error": "No JSON data provided"}, 400
            
            query = data.get('query')
            variables = data.get('variables')
            operation_name = data.get('operationName')
            
            if not query:
                return {"error": "No GraphQL query provided"}, 400
            
            # Execute query
            result = schema.execute(
                query,
                variable_values=variables,
                operation_name=operation_name
            )
            
            if result.errors:
                # Log errors
                for error in result.errors:
                    logger.error(f"GraphQL error: {error}")
                
                # Return errors
                errors = [str(error) for error in result.errors]
                return {"errors": errors}, 400
            
            # Return data
            return jsonify(result.data)
        
        except Exception as e:
            logger.error(f"Error processing GraphQL query: {e}")
            return {"error": str(e)}, 500