"""
GraphQL Route for BloxAPI

This module provides a GraphQL API endpoint for the BloxAPI.
It uses the graphene library to define a schema and execute queries.
"""

import json
import logging
from flask import request, jsonify
from flask_restful import Resource
from flask_graphql import GraphQLView
from utils.graphql_schema import schema
from utils.redis_cache import get_cache, cache_decorator

# Configure logging
logger = logging.getLogger(__name__)

class GraphQLResource(Resource):
    """
    GraphQL API endpoint for the BloxAPI
    """
    
    def get(self):
        """
        Handle GET requests for GraphQL (introspection)
        
        Returns:
            Response: GraphQL query result or error response
        """
        query = request.args.get('query')
        variables = request.args.get('variables')
        
        if variables:
            try:
                variables = json.loads(variables)
            except json.JSONDecodeError:
                return {"error": "Invalid variables JSON"}, 400
        
        return self._execute_query(query, variables)
    
    def post(self):
        """
        Handle POST requests for GraphQL queries
        
        Returns:
            Response: GraphQL query result or error response
        """
        # Get request JSON data
        data = request.get_json()
        
        if not data:
            return {"error": "No JSON data provided"}, 400
        
        query = data.get('query')
        variables = data.get('variables')
        
        return self._execute_query(query, variables)
    
    @cache_decorator("graphql", ttl=300)  # Cache for 5 minutes
    def _execute_query(self, query, variables=None):
        """
        Execute a GraphQL query and return the result
        
        Args:
            query (str): GraphQL query
            variables (dict, optional): Query variables
            
        Returns:
            dict: Query result or error response
        """
        if not query:
            return {"error": "No query provided"}, 400
        
        try:
            # Execute the query
            result = schema.execute(query, variable_values=variables)
            
            # Handle errors
            if result.errors:
                errors = [str(error) for error in result.errors]
                logger.error(f"GraphQL query errors: {errors}")
                return {
                    "errors": errors,
                    "data": result.data
                }, 400
            
            # Return successful result
            return {"data": result.data}
        
        except Exception as e:
            logger.exception(f"Error executing GraphQL query: {e}")
            return {"error": str(e)}, 500


# GraphQLView for the Flask app
graphql_view = GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True  # Enable GraphiQL interface for testing
)