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
from routes.groups import GroupResource, GroupMembersResource, GroupRolesResource
from routes.friends import FriendsResource, FriendRequestsResource
from routes.assets import AssetResource, AssetInfoResource
from routes.catalog import CatalogResource, CatalogSearchResource

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

# Web routes for documentation
@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

@app.route('/docs')
def documentation():
    from flask import render_template
    return render_template('documentation.html')

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
