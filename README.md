# 🟥 BloxAPI - Comprehensive Roblox API

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/Bogdan11212/BloxAPI?style=social)](https://github.com/Bogdan11212/BloxAPI/stargazers)
[![Forks](https://img.shields.io/github/forks/Bogdan11212/BloxAPI?style=social)](https://github.com/Bogdan11212/BloxAPI/network/members)
[![Contributors](https://img.shields.io/github/contributors/Bogdan11212/BloxAPI)](https://github.com/Bogdan11212/BloxAPI/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/Bogdan11212/BloxAPI)](https://github.com/Bogdan11212/BloxAPI/commits/master)

<img src="https://raw.githubusercontent.com/Bogdan11212/BloxAPI/main/docs/images/preview.png" alt="BloxAPI Preview" width="800px" />

</div>

<p align="center">A powerful, comprehensive API for interacting with the Roblox platform. BloxAPI provides developers with seamless access to Roblox data, functionality, and services through a well-organized REST API.</p>

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Integrations](#-integrations)
- [Examples](#-examples)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Features

- **Complete Platform Coverage**: Access virtually every aspect of the Roblox platform
- **Always Live Data**: Every request connects directly to Roblox's real API
- **User-Friendly Endpoints**: Clean, consistent, and well-documented API endpoints
- **Modern UI**: Interactive documentation and API explorer
- **Cross-Platform Support**: Use with any programming language via standard HTTP requests
- **Advanced Rate Limiting**: Built-in protection against hitting Roblox API limits
- **Robust Error Handling**: Comprehensive error reporting, retries and logging
- **External Service Integrations**: Connect with RoliMon's, Rblx.Trade, Roliverse and Rblx Values
- **Events System**: Track real-time events for users, games, and groups
- **Moderation Tools**: Content moderation, safety settings, and text filtering
- **Statistics API**: Get detailed analytics on games, players, and demographics
- **Server Management**: Monitor and control game server instances and VIP servers

## 💻 Installation

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Setup

1. Clone the repository
```bash
git clone https://github.com/Bogdan11212/BloxAPI.git
cd BloxAPI
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the development server
```bash
python main.py
```

The API will be available at `http://localhost:5000`

## 🚀 Quick Start

Here's a simple example of how to use BloxAPI to get information about a Roblox user:

```python
import requests

# Get user information
response = requests.get('http://localhost:5000/api/users/1')
user_data = response.json()
print(user_data)

# Search for users by name
response = requests.get('http://localhost:5000/api/users/search?keyword=builderman')
search_results = response.json()
print(search_results)
```

## 📖 API Documentation

Full API documentation is available at `/docs` when the server is running.

### Main Endpoints

- **Users**: `/api/users/{userId}`
- **Games**: `/api/games/{gameId}`
- **Groups**: `/api/groups/{groupId}`
- **Assets**: `/api/assets/{assetId}`
- **Catalog**: `/api/catalog/search`
- **Economy**: `/api/economy/currency/exchange-rate`
- **Badges**: `/api/badges/{badgeId}`
- **Events**: `/api/events/{entity_type}/{entity_id}`
- **Moderation**: `/api/moderation/content/{content_type}/{content_id}`
- **Statistics**: `/api/statistics/games/{universe_id}/universe`
- **Servers**: `/api/servers/games/{universe_id}/instances`
- **Social**: `/api/social/users/{user_id}/connections`
- **Monetization**: `/api/monetization/games/{universe_id}/developer-products`

## 🔄 Integrations

BloxAPI seamlessly integrates with popular third-party Roblox services:

### RoliMon's API Integration

Access item values, price history, and player stats with endpoints like:
- `/api/external/rolimon/items/{itemId}`
- `/api/external/rolimon/players/{userId}/value`

### Rblx.Trade Integration

Get trade advertisements and player reputation:
- `/api/external/rblx-trade/trade-ads`
- `/api/external/rblx-trade/players/{userId}/reputation`

### Roliverse Integration

Access market trends and demand indexes:
- `/api/external/roliverse/market/trends`
- `/api/external/roliverse/items/{itemId}/demand`

### Rblx Values Integration

Check item stability and projected status:
- `/api/external/rblx-values/items/{itemId}/stability`
- `/api/external/rblx-values/market/rising`

## 🔍 Examples

### Example 1: Get User's Friends

```javascript
fetch('http://localhost:5000/api/users/1/friends')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Example 2: Search the Catalog

```javascript
fetch('http://localhost:5000/api/catalog/search?keyword=dominus&category=hats&limit=25')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Example 3: Get Game Statistics

```javascript
fetch('http://localhost:5000/api/statistics/games/1234567890/universe')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Example 4: Check Content Moderation Status

```javascript
fetch('http://localhost:5000/api/moderation/content/asset/1234567')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Example 5: Get Game Server Instances

```javascript
fetch('http://localhost:5000/api/servers/games/1234567890/instances?limit=10')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Example 6: Get Item Value from RoliMon's

```javascript
fetch('http://localhost:5000/api/external/rolimon/items/1365767/history')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🛣️ Roadmap

- [ ] Authentication system for higher rate limits
- [ ] Webhook support for real-time notifications
- [ ] Caching layer for improved performance
- [ ] GraphQL endpoint
- [ ] Mobile SDK
- [ ] Admin dashboard for monitoring API usage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📋 API Categories

- **Users**: User profiles, search, and authentication data
- **Games**: Game details, analytics, and statistics
- **Groups**: Group information, roles, and membership data
- **Assets**: Item details, ownership, and catalog information
- **Economy**: Marketplace data, currency exchange, and trading information
- **Inventory**: User item ownership and collections
- **Badges**: Badge details and user badge data
- **Analytics**: Performance metrics and usage statistics
- **Notifications**: User notification system integration
- **Chat**: Messaging system integration
- **Events**: Real-time event notifications for users, games, and groups
- **Moderation**: Content moderation tools and safety features
- **Statistics**: Detailed game analytics and player metrics
- **Servers**: Game server management and VIP server control
- **Social**: User social connections and friend recommendations
- **Monetization**: Developer products, game passes, and premium payouts
- **Subscriptions**: Premium subscription features and benefits
- **User Profiles**: Extended profile information and settings

## 🔧 Recent Improvements

### API Expansion (200+ New Endpoints)
- **Events System**: New endpoints for tracking user, game, and group events with real-time notifications
- **Moderation API**: Content moderation tools, safety settings, and text filtering capabilities
- **Statistics System**: Enhanced game analytics with playtime tracking, retention rates, and demographic data
- **Server Management**: New endpoints for monitoring and controlling game server instances
- **Social Connections**: Friend recommendations, social graph analysis, and connection management
- **Monetization Tools**: Developer product endpoints, premium payout tracking, and game pass analytics
- **Subscriptions**: Premium subscription features and membership benefits tracking
- **User Profiles**: Extended profile data, settings management, and privacy controls

### API Reliability Enhancements
- **Removed Demo Mode**: All endpoints now connect directly to the real Roblox API for authentic data
- **Fixed Critical Endpoints**: Addressed issues with User Search, User Friends, Game Details, and other crucial endpoints
- **Enhanced Error Handling**: Implemented comprehensive error detection, reporting and recovery
- **Intelligent Retries**: Added automatic retry mechanism with exponential backoff for transient network issues
- **Input Validation**: Added proper parameter validation and sanitization to prevent errors
- **Improved Logging**: Enhanced logging for better troubleshooting and monitoring
- **API Standardization**: Ensured consistent response formats across all endpoints

### External Integrations
- **RoliMon's Integration**: Complete overhaul of item value tracking endpoints
- **Rblx.Trade Connection**: Improved trade advertisement and player reputation endpoints
- **Roliverse API**: Added new endpoints for market trends and demand insights
- **Rblx Values API**: Added support for item stability metrics and projected status

## 🔧 JavaScript Client Library

BloxAPI includes a JavaScript library for browser-based applications, making it easy to integrate with web projects:

```javascript
// Get user information
BloxAPI.users.getUser(1234567)
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

## 🔄 Rate Limiting and Error Handling

BloxAPI implements advanced rate limiting and error handling to ensure reliable and fair usage:

### Rate Limiting
- 60 requests per minute for standard usage
- Responses include rate limit headers for monitoring usage
- Built-in handling of Roblox API rate limits with automatic retries

### Error Handling
- Automatic retries for transient network errors (up to 3 attempts with exponential backoff)
- Detailed error messages with HTTP status codes and contextual information
- Consistent error response format across all endpoints
- Special handling for common error scenarios (e.g., resource not found, invalid parameters)
- Detailed logging for troubleshooting

## 📞 Contact

GitHub: [@Bogdan11212](https://github.com/Bogdan11212)

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Bogdan11212/BloxAPI&type=Date)](https://star-history.com/#Bogdan11212/BloxAPI&Date)