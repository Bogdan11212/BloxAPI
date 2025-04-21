# 🟥 BloxAPI - Comprehensive Roblox API

<div align="center">

<img src="https://raw.githubusercontent.com/Bogdan11212/BloxAPI/main/docs/images/preview.png" alt="BloxAPI Preview" width="800px" />

<h3>Your Ultimate Gateway to the Roblox Platform</h3>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/Bogdan11212/BloxAPI?style=social)](https://github.com/Bogdan11212/BloxAPI/stargazers)
[![Forks](https://img.shields.io/github/forks/Bogdan11212/BloxAPI?style=social)](https://github.com/Bogdan11212/BloxAPI/network/members)
[![Contributors](https://img.shields.io/github/contributors/Bogdan11212/BloxAPI)](https://github.com/Bogdan11212/BloxAPI/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/Bogdan11212/BloxAPI)](https://github.com/Bogdan11212/BloxAPI/commits/master)
[![Open Issues](https://img.shields.io/github/issues/Bogdan11212/BloxAPI)](https://github.com/Bogdan11212/BloxAPI/issues)
[![Discussions](https://img.shields.io/github/discussions/Bogdan11212/BloxAPI)](https://github.com/Bogdan11212/BloxAPI/discussions)

<br>

[![Deploy to Replit](https://repl.it/badge/github/Bogdan11212/BloxAPI)](https://repl.it/github/Bogdan11212/BloxAPI)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Bogdan11212/BloxAPI)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Bogdan11212/BloxAPI)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FBogdan11212%2FBloxAPI)
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Bogdan11212/BloxAPI)

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

<div align="center">
  <img src="https://raw.githubusercontent.com/Bogdan11212/BloxAPI/main/docs/images/features.svg" alt="BloxAPI Features" width="200px" />
</div>

<table>
  <tr>
    <td width="33%" align="center">
      <h3>🌐 Platform Coverage</h3>
      <p>Access virtually every aspect of the Roblox platform with comprehensive API coverage</p>
    </td>
    <td width="33%" align="center">
      <h3>🔄 Live Data</h3>
      <p>Every request connects directly to Roblox's real API for up-to-date information</p>
    </td>
    <td width="33%" align="center">
      <h3>📊 Analytics</h3>
      <p>Get detailed statistics on games, players, and demographics</p>
    </td>
  </tr>
  <tr>
    <td width="33%" align="center">
      <h3>🛡️ Rate Limiting</h3>
      <p>Built-in protection against hitting Roblox API limits with intelligent retries</p>
    </td>
    <td width="33%" align="center">
      <h3>🔌 Integrations</h3>
      <p>Connect with RoliMon's, Rblx.Trade, Roliverse and Rblx Values</p>
    </td>
    <td width="33%" align="center">
      <h3>📱 Cross-Platform</h3>
      <p>Use with any programming language via standard HTTP requests</p>
    </td>
  </tr>
  <tr>
    <td width="33%" align="center">
      <h3>🚨 Error Handling</h3>
      <p>Comprehensive error reporting, automatic retries and detailed logging</p>
    </td>
    <td width="33%" align="center">
      <h3>🔔 Events</h3>
      <p>Track real-time events for users, games, and groups</p>
    </td>
    <td width="33%" align="center">
      <h3>🖥️ Server Management</h3>
      <p>Monitor and control game server instances and VIP servers</p>
    </td>
  </tr>
</table>

## 💻 Installation

<div align="center">
  <img src="https://raw.githubusercontent.com/Bogdan11212/BloxAPI/main/docs/images/installation.svg" alt="Installation" width="180px" />
</div>

### Multiple Installation Options

<details open>
  <summary><strong>🐍 Standard Python Installation</strong></summary>
  
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
</details>

<details>
  <summary><strong>🐳 Docker Installation</strong></summary>
  
  ### Prerequisites
  - Docker

  ### Setup
  1. Clone the repository
  ```bash
  git clone https://github.com/Bogdan11212/BloxAPI.git
  cd BloxAPI
  ```

  2. Build and run with Docker Compose
  ```bash
  docker-compose up --build
  ```

  The API will be available at `http://localhost:5000`
</details>

<details>
  <summary><strong>☁️ One-Click Cloud Deployment</strong></summary>
  
  ### Options
  - [Deploy to Replit](https://repl.it/github/Bogdan11212/BloxAPI)
  - [Deploy to Heroku](https://heroku.com/deploy?template=https://github.com/Bogdan11212/BloxAPI)
  - [Deploy to Render](https://render.com/deploy?repo=https://github.com/Bogdan11212/BloxAPI)
  - [Deploy with Vercel](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FBogdan11212%2FBloxAPI)
</details>

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

<div align="center">
  <img src="https://raw.githubusercontent.com/Bogdan11212/BloxAPI/main/docs/images/documentation.svg" alt="API Documentation" width="200px" />
</div>

Full interactive API documentation with request/response examples and schema information is available at **`/docs`** when the server is running.

<div align="center">
  <img src="https://raw.githubusercontent.com/Bogdan11212/BloxAPI/main/docs/images/api-screenshot.png" alt="API Documentation Screenshot" width="800px" />
</div>

### Core API Categories

<div class="endpoint-grid">
  <table>
    <tr>
      <th width="25%" align="center">🧑‍🤝‍🧑 User & Social</th>
      <th width="25%" align="center">🎮 Games & Servers</th>
      <th width="25%" align="center">💰 Economy & Assets</th>
      <th width="25%" align="center">📊 Analytics & Events</th>
    </tr>
    <tr valign="top">
      <td>
        <ul>
          <li><code>/api/users/{userId}</code></li>
          <li><code>/api/users/search</code></li>
          <li><code>/api/users/{userId}/friends</code></li>
          <li><code>/api/groups/{groupId}</code></li>
          <li><code>/api/social/users/{userId}/connections</code></li>
        </ul>
      </td>
      <td>
        <ul>
          <li><code>/api/games/{gameId}</code></li>
          <li><code>/api/games/{universeId}/details</code></li>
          <li><code>/api/servers/games/{universeId}/instances</code></li>
          <li><code>/api/games/{universeId}/servers/vip</code></li>
        </ul>
      </td>
      <td>
        <ul>
          <li><code>/api/assets/{assetId}</code></li>
          <li><code>/api/catalog/search</code></li>
          <li><code>/api/economy/currency/exchange-rate</code></li>
          <li><code>/api/inventory/users/{userId}/assets</code></li>
        </ul>
      </td>
      <td>
        <ul>
          <li><code>/api/statistics/games/{universeId}/universe</code></li>
          <li><code>/api/analytics/games/{universeId}/{metricType}</code></li>
          <li><code>/api/events/{entityType}/{entityId}</code></li>
          <li><code>/api/notifications/users/{userId}</code></li>
        </ul>
      </td>
    </tr>
  </table>
</div>

### Advanced API Features

<details>
  <summary><strong>🔐 Authentication & Security</strong></summary>
  <ul>
    <li><code>/api/auth/token</code> - Get an authentication token</li>
    <li><code>/api/auth/validate</code> - Validate a token</li>
    <li><code>/api/auth/refresh</code> - Refresh an authentication token</li>
    <li><code>/api/users/{userId}/security/settings</code> - Get security settings</li>
    <li><code>/api/moderation/content/{contentType}/{contentId}</code> - Check content moderation status</li>
  </ul>
</details>

<details>
  <summary><strong>👥 Group Management</strong></summary>
  <ul>
    <li><code>/api/groups/{groupId}/users</code> - Get group members</li>
    <li><code>/api/groups/{groupId}/roles</code> - Get group roles</li>
    <li><code>/api/groups/{groupId}/wall/posts</code> - Get group wall posts</li>
    <li><code>/api/groups/{groupId}/relationships</code> - Get group relationships</li>
    <li><code>/api/groups/{groupId}/audit-log</code> - Get group audit log</li>
  </ul>
</details>

<details>
  <summary><strong>💹 Developer Economics</strong></summary>
  <ul>
    <li><code>/api/monetization/games/{universeId}/developer-products</code> - Get developer products</li>
    <li><code>/api/monetization/games/{universeId}/gamepasses</code> - Get game passes</li>
    <li><code>/api/monetization/games/{universeId}/revenue</code> - Get revenue information</li>
    <li><code>/api/economy/assets/{assetId}/resellers</code> - Get asset resellers</li>
    <li><code>/api/economy/assets/{assetId}/price-history</code> - Get asset price history</li>
  </ul>
</details>

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

<div align="center">
  <img src="https://raw.githubusercontent.com/Bogdan11212/BloxAPI/main/docs/images/code-examples.svg" alt="Code Examples" width="200px" />
</div>

<table width="100%">
<tr>
<td width="50%" valign="top">

### 💬 Get User's Friends

```javascript
fetch('http://localhost:5000/api/users/1/friends')
  .then(response => response.json())
  .then(data => console.log(data));
```

### 🎮 Get Game Statistics

```javascript
fetch('http://localhost:5000/api/statistics/games/1234567890/universe')
  .then(response => response.json())
  .then(data => console.log(data));
```

### 🏆 Get Game Server Instances

```javascript
fetch('http://localhost:5000/api/servers/games/1234567890/instances?limit=10')
  .then(response => response.json())
  .then(data => console.log(data));
```

</td>
<td width="50%" valign="top">

### 🛒 Search the Catalog

```javascript
fetch('http://localhost:5000/api/catalog/search?keyword=dominus&category=hats&limit=25')
  .then(response => response.json())
  .then(data => console.log(data));
```

### 🛡️ Check Content Moderation Status

```javascript
fetch('http://localhost:5000/api/moderation/content/asset/1234567')
  .then(response => response.json())
  .then(data => console.log(data));
```

### 💰 Get Item Value from RoliMon's

```javascript
fetch('http://localhost:5000/api/external/rolimon/items/1365767/history')
  .then(response => response.json())
  .then(data => console.log(data));
```

</td>
</tr>
</table>

<div align="center">
  <details>
    <summary><strong>📚 View More Examples</strong></summary>
    <br>
    
### 📊 Track User Analytics
```javascript
fetch('http://localhost:5000/api/analytics/users/1234567/visits?time_frame=past30days')
  .then(response => response.json())
  .then(data => console.log(data));
```

### 👥 Get Group Members
```javascript
fetch('http://localhost:5000/api/groups/1234567/members?limit=100')
  .then(response => response.json())
  .then(data => console.log(data));
```

### 🧩 Get Asset Information
```javascript
fetch('http://localhost:5000/api/assets/123456789/info?include_bundles=true')
  .then(response => response.json())
  .then(data => console.log(data));
```
  </details>
</div>

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