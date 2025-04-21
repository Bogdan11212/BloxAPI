<div align="center">
  <img src="docs/images/logo.png" alt="BloxAPI Logo" width="200"/>
  <h1>BloxAPI</h1>
  <p>A comprehensive Python-based Roblox API integration toolkit with 2000+ functions</p>
  
  <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 15px; margin-bottom: 15px;">
    <a href="https://github.com/Bogdan11212/BloxAPI/actions/workflows/python-tests.yml">
      <img src="https://img.shields.io/github/actions/workflow/status/Bogdan11212/BloxAPI/python-tests.yml?label=tests&style=for-the-badge&logo=github" alt="Python Tests">
    </a>
    <a href="https://github.com/Bogdan11212/BloxAPI/actions/workflows/docker-publish.yml">
      <img src="https://img.shields.io/github/actions/workflow/status/Bogdan11212/BloxAPI/docker-publish.yml?label=build&style=for-the-badge&logo=docker" alt="Docker">
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/github/license/Bogdan11212/BloxAPI?style=for-the-badge" alt="License">
    </a>
    <a href="https://github.com/Bogdan11212/BloxAPI">
      <img src="https://img.shields.io/badge/version-2.0.0-blue?style=for-the-badge&logo=semver" alt="Version">
    </a>
    <a href="https://github.com/Bogdan11212/BloxAPI">
      <img src="https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11-blue?style=for-the-badge&logo=python" alt="Python Version">
    </a>
    <a href="docs/documentation.html">
      <img src="https://img.shields.io/badge/docs-comprehensive-brightgreen?style=for-the-badge&logo=bookstack" alt="Documentation Status">
    </a>
    <a href="docs/coverage.html">
      <img src="https://img.shields.io/badge/coverage-95%25-success?style=for-the-badge&logo=codecov" alt="Code Coverage">
    </a>
  </div>
  
  <div>
    <img src="docs/images/api-overview.png" alt="API Overview" width="600" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
  </div>
</div>

## 🚀 Features

BloxAPI provides a robust interface to the Roblox platform with:

- **Comprehensive Endpoint Coverage** - Access all major Roblox API endpoints through a simple, unified interface
- **2000+ API Functions** - Extensive library of over 2,000 API functions covering every aspect of the Roblox platform
- **Intelligent Rate Limiting** - Automatic handling of Roblox API rate limits with queuing and retries
- **Efficient Caching** - Configurable multi-level caching system to minimize API calls
- **Advanced Analytics** - Deep insights into user behavior, retention, and monetization
- **Platform Integrations** - Seamless connectivity with external gaming platforms and services
- **Business Intelligence** - Data warehousing, transformations, and visualization tools
- **Content Management** - Comprehensive tools for managing and publishing content
- **Security Tools** - Robust security features including threat detection and access control
- **Robust Error Handling** - Detailed error reporting and automatic retries for transient failures
- **Type Hints & Documentation** - Fully typed API with comprehensive documentation
- **Async & Sync Support** - Both synchronous and asynchronous interfaces
- **Extensible Design** - Easy to extend for custom use cases
- **Cross-Platform** - Works on Windows, macOS, and Linux

## 📦 Installation

```bash
# Using pip
pip install bloxapi

# Using poetry
poetry add bloxapi

# From source
git clone https://github.com/Bogdan11212/BloxAPI.git
cd BloxAPI
pip install -e .
```

## 🛠️ Quick Start

```python
from bloxapi import BloxAPI

# Initialize the client
api = BloxAPI()

# Get user information
user = api.users.get_by_username("Builderman")
print(f"User ID: {user.id}")
print(f"Display Name: {user.display_name}")

# Get game details
game = api.games.get_details(920587237)
print(f"Game Name: {game.name}")
print(f"Player Count: {game.playing}")

# Get user's inventory
inventory = api.inventory.get_collectibles(user.id)
for item in inventory:
    print(f"{item.name} (Asset ID: {item.asset_id})")
```

## 🔍 Usage Examples

### Working with Users

```python
# Get multiple users by IDs
users = api.users.get_users([1, 156, 123456])

# Check online status
presence = api.presence.get_user_presence(user.id)
print(f"Is online: {presence.is_online}")
print(f"Last location: {presence.last_location}")

# Get user's friends
friends = api.friends.get_friends(user.id)
for friend in friends:
    print(f"{friend.display_name} (User ID: {friend.id})")
```

### Working with Games

```python
# Search for games
games = api.games.search(keyword="simulator", sort_by="most_played")

# Get game badges
badges = api.badges.get_game_badges(game.id)
for badge in badges:
    print(f"{badge.name} - {badge.description}")

# Get game analytics (requires game ownership)
analytics = api.analytics.get_game_analytics(game.id, "player_retention")
```

### Working with Groups

```python
# Get group information
group = api.groups.get_group(4199740)
print(f"Group Name: {group.name}")
print(f"Member Count: {group.member_count}")

# Get group members
members = api.groups.get_group_members(group.id, role="Admin")

# Join a group
api.groups.join_group(group.id)
```

### Advanced Analytics

```python
# Get cross-platform analytics
cross_platform = api.integrated_analytics.get_cross_platform(game.id, start_date="2025-01-01", end_date="2025-04-01")
print(f"Mobile users: {cross_platform.mobile_percentage}%")
print(f"Console users: {cross_platform.console_percentage}%")

# Analyze player retention
retention = api.integrated_analytics.get_retention_cohorts(game.id, granularity="week")
print(f"Week 1 retention: {retention.cohorts[0].retention_rate}%")

# Predict player churn
churn_prediction = api.integrated_analytics.predict_churn(game.id, prediction_window=30)
for player in churn_prediction.at_risk_players:
    print(f"Player {player.username} has {player.churn_probability * 100}% chance of churning")
```

### Platform Integrations

```python
# Get available platforms
platforms = api.platforms.get_available_platforms()
for platform in platforms:
    print(f"Platform: {platform.name}, Status: {platform.status}")

# Import friends from external platform
friends = api.platforms.get_friends(user.id, platform_id="steam")
api.platforms.import_friends(user.id, platform_id="steam", friend_ids=[f.id for f in friends[:5]])

# Sync game data with external platforms
api.platforms.sync_game(game.id, platform_id="xbox", sync_config={
    "achievements": True,
    "leaderboards": True
})
```

### Content Management

```python
# Get content library
content = api.content.get_library(user_id=user.id, content_type="Model")
for item in content:
    print(f"{item.name} (Created: {item.created_at})")

# Upload new content
new_model = api.content.upload({
    "content_type": "Model",
    "name": "My Awesome Character",
    "description": "A detailed character model",
    "file_data": encoded_file_data,
    "tags": ["character", "humanoid", "detailed"]
})
print(f"Uploaded model ID: {new_model.id}")

# Manage collaborators
api.content.add_collaborator(content_id=new_model.id, user_id=friend.id, permission_level="Edit")
```

### Business Intelligence

```python
# Configure data pipeline
pipeline = api.bi.create_pipeline(universe_id=game.id, {
    "pipeline_name": "Daily Player Metrics",
    "pipeline_steps": [
        {"type": "extract", "source": "game_analytics", "metrics": ["playtime", "retention"]},
        {"type": "transform", "aggregation": "daily"},
        {"type": "load", "destination": "data_warehouse"}
    ],
    "schedule": {"frequency": "daily", "time": "04:00:00"}
})

# Execute ad-hoc query
result = api.bi.execute_query(
    query="SELECT date, count(distinct user_id) FROM player_sessions WHERE universe_id = :universe_id GROUP BY date",
    data_source="data_warehouse",
    parameters={"universe_id": game.id}
)
for row in result:
    print(f"Date: {row.date}, Active Users: {row.count}")
```

## 🔌 Advanced Features

### Authentication

```python
# Authenticate with cookies
api = BloxAPI(cookies={".ROBLOSECURITY": "your_cookie_here"})

# Authenticate with API key (for developer endpoints)
api = BloxAPI(api_key="your_api_key_here")

# Get authenticated user info
me = api.users.get_authenticated_user()
```

### Rate Limiting

```python
# Configure rate limits
api = BloxAPI(
    rate_limit=True,
    max_requests=100,
    rate_limit_window=60  # seconds
)
```

### Caching

```python
# Configure caching
api = BloxAPI(
    cache=True,
    cache_expire={
        "users": 3600,  # 1 hour for users
        "games": 300,   # 5 minutes for games
        "default": 1800 # 30 minutes default
    },
    cache_backend="redis",
    redis_url="redis://localhost:6379/0"
)
```

### Asynchronous Usage

```python
import asyncio
from bloxapi.async_client import AsyncBloxAPI

async def main():
    api = AsyncBloxAPI()
    
    # Fetch multiple resources concurrently
    user, game = await asyncio.gather(
        api.users.get_by_username("Builderman"),
        api.games.get_details(920587237)
    )
    
    print(f"User: {user.display_name}, Game: {game.name}")

# Run the async function
asyncio.run(main())
```

## 🌐 API Reference

Visit our [API Reference](docs/api_reference.html) for complete documentation of all available methods and parameters. The full API documentation is included in this repository.

## 🏗️ Architecture

For a detailed overview of the project architecture, see [ARCHITECTURE.md](ARCHITECTURE.md).

## 🤝 Contributing

Contributions are welcome! Please check out our [Contributing Guide](CONTRIBUTING.md) for guidelines.

## 🔐 Security

For information on reporting security vulnerabilities, see our [Security Policy](SECURITY.md).

## 📱 Integrations

BloxAPI seamlessly integrates with popular web frameworks and tools:

### Flask Integration

```python
from flask import Flask
from bloxapi.integrations.flask import init_bloxapi

app = Flask(__name__)
api = init_bloxapi(app)

@app.route('/user/<username>')
def get_user(username):
    user = api.users.get_by_username(username)
    return {
        "id": user.id,
        "displayName": user.display_name,
        "avatar": user.avatar_url
    }
```

### Django Integration

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'bloxapi.integrations.django',
]

BLOXAPI_CONFIG = {
    'cache': True,
    'rate_limit': True,
}

# views.py
from django.http import JsonResponse
from bloxapi.integrations.django import get_api

def user_profile(request, username):
    api = get_api()
    user = api.users.get_by_username(username)
    return JsonResponse({
        "id": user.id,
        "displayName": user.display_name,
    })
```

## 📊 Deployment Options

<div align="center">
  <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
    <a href="https://github.com/Bogdan11212/BloxAPI/blob/main/docs/deployment/heroku.md">
      <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku" height="32">
    </a>
    <a href="https://github.com/Bogdan11212/BloxAPI/blob/main/docs/deployment/render.md">
      <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" height="32">
    </a>
    <a href="https://github.com/Bogdan11212/BloxAPI/blob/main/docs/deployment/railway.md">
      <img src="https://railway.app/button.svg" alt="Deploy on Railway" height="32">
    </a>
    <a href="https://github.com/Bogdan11212/BloxAPI/blob/main/docs/deployment/vercel.md">
      <img src="https://vercel.com/button" alt="Deploy with Vercel" height="32">
    </a>
    <a href="https://github.com/Bogdan11212/BloxAPI/blob/main/docs/deployment/netlify.md">
      <img src="https://www.netlify.com/img/deploy/button.svg" alt="Deploy to Netlify" height="32">
    </a>
  </div>
  
  <p style="margin-top: 10px;">
    See our <a href="docs/deployment/index.html">deployment documentation</a> for more detailed instructions.
  </p>
</div>

## 🐳 Docker

```bash
# Pull the image
docker pull ghcr.io/bogdan11212/bloxapi:latest

# Run the container
docker run -p 5000:5000 -e SECRET_KEY=your_secret_key ghcr.io/bogdan11212/bloxapi:latest

# Using Docker Compose
docker-compose up -d
```

The Docker image is continuously built and published with each release. You can also build your own image using the provided Dockerfile.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ by the BloxAPI team</sub>
</div>