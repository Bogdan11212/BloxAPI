"""
Widget Builder for BloxAPI

This script creates SVG images and badges for the BloxAPI project README.
It generates the following assets:
1. Logo SVG
2. Feature icons
3. README badges
4. Deployment buttons
"""

import os
import argparse
import json
import subprocess
import textwrap
from pathlib import Path
from datetime import datetime


# Create directories if they don't exist
def ensure_dirs():
    """Create necessary directories if they don't exist"""
    dirs = [
        'docs/images',
        'docs/badges',
        'docs/deployment',
        'static/images/icons',
    ]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Directory structure created/verified")


# SVG Logo Creator
def create_logo():
    """Create the BloxAPI logo as SVG"""
    logo_path = 'docs/images/logo.svg'
    
    # Create a simple yet attractive logo
    logo_svg = """<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#4f46e5" />
            <stop offset="100%" stop-color="#7c3aed" />
        </linearGradient>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.3" />
        </filter>
    </defs>
    <rect x="40" y="40" width="120" height="120" rx="16" fill="url(#gradient)" filter="url(#shadow)" />
    <path d="M75 70 L75 130 L90 130 L90 105 L110 105 L110 130 L125 130 L125 70 L110 70 L110 90 L90 90 L90 70 Z" 
          fill="white" />
    <circle cx="140" cy="70" r="10" fill="#10b981" />
</svg>"""
    
    with open(logo_path, 'w') as f:
        f.write(logo_svg)
    
    # Convert SVG to PNG for GitHub display
    try:
        png_path = logo_path.replace('.svg', '.png')
        subprocess.run(['rsvg-convert', '-w', '200', '-h', '200', logo_path, '-o', png_path], check=True)
        print(f"✓ Logo created at {logo_path} and {png_path}")
    except Exception as e:
        print(f"⚠️ Could not convert SVG to PNG: {e}")
        print(f"✓ Logo created at {logo_path} only")


# Create Feature Icons
def create_feature_icons():
    """Create icons for features section in README"""
    icons = {
        'architecture': """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#3b82f6" />
                    <stop offset="100%" stop-color="#2563eb" />
                </linearGradient>
            </defs>
            <rect x="10" y="10" width="80" height="80" rx="8" fill="url(#grad1)" />
            <rect x="25" y="25" width="20" height="50" rx="4" fill="white" opacity="0.9" />
            <rect x="55" y="25" width="20" height="50" rx="4" fill="white" opacity="0.9" />
            <rect x="30" y="35" width="10" height="5" rx="1" fill="#3b82f6" />
            <rect x="30" y="45" width="10" height="5" rx="1" fill="#3b82f6" />
            <rect x="30" y="55" width="10" height="5" rx="1" fill="#3b82f6" />
            <rect x="60" y="35" width="10" height="5" rx="1" fill="#3b82f6" />
            <rect x="60" y="45" width="10" height="5" rx="1" fill="#3b82f6" />
            <rect x="60" y="55" width="10" height="5" rx="1" fill="#3b82f6" />
        </svg>""",
        
        'code-examples': """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
            <defs>
                <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#10b981" />
                    <stop offset="100%" stop-color="#059669" />
                </linearGradient>
            </defs>
            <rect x="10" y="10" width="80" height="80" rx="8" fill="url(#grad2)" />
            <text x="30" y="40" font-family="monospace" font-size="14" fill="white">&lt;/&gt;</text>
            <rect x="25" y="50" width="50" height="3" rx="1.5" fill="white" opacity="0.7" />
            <rect x="25" y="58" width="40" height="3" rx="1.5" fill="white" opacity="0.7" />
            <rect x="25" y="66" width="45" height="3" rx="1.5" fill="white" opacity="0.7" />
        </svg>""",
        
        'documentation': """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
            <defs>
                <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#f59e0b" />
                    <stop offset="100%" stop-color="#d97706" />
                </linearGradient>
            </defs>
            <rect x="10" y="10" width="80" height="80" rx="8" fill="url(#grad3)" />
            <rect x="25" y="25" width="50" height="7" rx="3.5" fill="white" opacity="0.9" />
            <rect x="25" y="37" width="40" height="3" rx="1.5" fill="white" opacity="0.7" />
            <rect x="25" y="44" width="45" height="3" rx="1.5" fill="white" opacity="0.7" />
            <rect x="25" y="51" width="35" height="3" rx="1.5" fill="white" opacity="0.7" />
            <rect x="25" y="63" width="20" height="12" rx="2" fill="white" opacity="0.9" />
            <rect x="50" y="63" width="20" height="12" rx="2" fill="white" opacity="0.9" />
        </svg>""",
        
        'features': """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
            <defs>
                <linearGradient id="grad4" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ec4899" />
                    <stop offset="100%" stop-color="#db2777" />
                </linearGradient>
            </defs>
            <rect x="10" y="10" width="80" height="80" rx="8" fill="url(#grad4)" />
            <circle cx="35" cy="35" r="10" fill="white" opacity="0.9" />
            <circle cx="65" cy="35" r="10" fill="white" opacity="0.9" />
            <circle cx="35" cy="65" r="10" fill="white" opacity="0.9" />
            <circle cx="65" cy="65" r="10" fill="white" opacity="0.9" />
            <circle cx="35" cy="35" r="5" fill="#ec4899" />
            <circle cx="65" cy="35" r="5" fill="#ec4899" />
            <circle cx="35" cy="65" r="5" fill="#ec4899" />
            <circle cx="65" cy="65" r="5" fill="#ec4899" />
        </svg>""",
        
        'installation': """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
            <defs>
                <linearGradient id="grad5" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#8b5cf6" />
                    <stop offset="100%" stop-color="#7c3aed" />
                </linearGradient>
            </defs>
            <rect x="10" y="10" width="80" height="80" rx="8" fill="url(#grad5)" />
            <rect x="30" y="25" width="40" height="50" rx="4" fill="white" opacity="0.9" />
            <rect x="35" y="35" width="30" height="5" rx="2.5" fill="#8b5cf6" />
            <rect x="35" y="45" width="30" height="5" rx="2.5" fill="#8b5cf6" />
            <rect x="35" y="55" width="30" height="5" rx="2.5" fill="#8b5cf6" />
            <path d="M50 17 L60 30 L40 30 Z" fill="white" opacity="0.9" />
        </svg>"""
    }
    
    for name, svg_content in icons.items():
        svg_path = f'docs/images/{name}.svg'
        with open(svg_path, 'w') as f:
            f.write(svg_content)
        
        # Convert SVG to PNG for better compatibility
        try:
            png_path = svg_path.replace('.svg', '.png')
            subprocess.run(['rsvg-convert', '-w', '100', '-h', '100', svg_path, '-o', png_path], check=True)
        except Exception as e:
            print(f"⚠️ Could not convert SVG to PNG for {name}: {e}")
    
    print(f"✓ Feature icons created in docs/images/")


# Create Deployment Documentation Files
def create_deployment_docs():
    """Create documentation files for deployment options"""
    deployment_platforms = ['heroku', 'render', 'railway', 'vercel', 'netlify']
    
    # Create index.html for deployment documentation
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BloxAPI Deployment Options</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #4f46e5;
            border-bottom: 2px solid #4f46e5;
            padding-bottom: 10px;
        }
        h2 {
            color: #7c3aed;
            margin-top: 30px;
        }
        a {
            color: #4f46e5;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .platform-list {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 20px;
        }
        .platform-card {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
            width: calc(50% - 15px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .platform-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        @media (max-width: 600px) {
            .platform-card {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <h1>BloxAPI Deployment Options</h1>
    <p>BloxAPI can be deployed to various platforms with minimal configuration. Choose the platform that best fits your needs.</p>
    
    <div class="platform-list">
"""
    
    for platform in deployment_platforms:
        index_html += f"""        <div class="platform-card">
            <h2>{platform.capitalize()}</h2>
            <p>Deploy BloxAPI to {platform.capitalize()} with one click.</p>
            <a href="{platform}.html">View {platform.capitalize()} deployment guide →</a>
        </div>
"""
    
    index_html += """    </div>
    
    <h2>General Deployment Requirements</h2>
    <ul>
        <li><strong>Python 3.7+</strong> - BloxAPI requires Python 3.7 or higher</li>
        <li><strong>PostgreSQL database</strong> - For storing user data and analytics</li>
        <li><strong>Environment Variables</strong> - API keys and configuration settings</li>
    </ul>
    
    <h2>Environment Variables</h2>
    <p>The following environment variables should be configured regardless of deployment platform:</p>
    <ul>
        <li><code>SECRET_KEY</code> - A secret key for secure session handling</li>
        <li><code>DATABASE_URL</code> - PostgreSQL connection string</li>
        <li><code>ROBLOX_API_KEY</code> - Your Roblox API key (optional)</li>
        <li><code>REDIS_URL</code> - Redis connection string (optional, for caching)</li>
    </ul>
</body>
</html>"""
    
    with open('docs/deployment/index.html', 'w') as f:
        f.write(index_html)
    
    # Create individual deployment guides
    for platform in deployment_platforms:
        platform_doc = f"""# Deploying BloxAPI to {platform.capitalize()}

This guide will help you deploy BloxAPI to {platform.capitalize()}.

## Prerequisites

- A {platform.capitalize()} account
- Git repository with your BloxAPI fork
- Understanding of basic deployment concepts

## Deployment Steps

1. Fork the BloxAPI repository
2. Set up your {platform.capitalize()} account
3. Connect your repository to {platform.capitalize()}
4. Configure the necessary environment variables
5. Deploy the application

## Environment Variables

Make sure to set these environment variables:

- `SECRET_KEY`: A secure random string
- `DATABASE_URL`: Your PostgreSQL connection string
- `ROBLOX_API_KEY`: Your Roblox API key (optional)
- `REDIS_URL`: Redis connection string (optional, for caching)

## Additional Configuration

Refer to the {platform.capitalize()} documentation for platform-specific settings and optimizations.
"""
        with open(f'docs/deployment/{platform}.md', 'w') as f:
            f.write(platform_doc)
    
    print(f"✓ Deployment documentation created in docs/deployment/")


# Main function
def main():
    """Main function to create all assets"""
    ensure_dirs()
    create_logo()
    create_feature_icons()
    create_deployment_docs()
    print("\n✅ All README assets created successfully!")


if __name__ == "__main__":
    main()