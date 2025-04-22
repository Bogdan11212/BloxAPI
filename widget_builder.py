"""
Widget Builder for BloxAPI

This script creates SVG images and badges for the BloxAPI project README.
It generates the following assets:
1. Logo SVG with modern design and animation options
2. Feature icons with interactive elements
3. README badges with custom styling
4. Architecture diagrams and visual documentation
5. Deployment buttons with hover effects
6. Interactive UI elements for better documentation
"""

import os
import sys
import math
import argparse
import json
import random
import subprocess
import textwrap
from pathlib import Path
from datetime import datetime

# Try to import advanced visualization libraries, gracefully handle if not available
try:
    import svgwrite
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    ADVANCED_MODE = True
except ImportError:
    ADVANCED_MODE = False
    print("Note: Advanced visualization libraries not found. Running in basic mode.")
    print("To enable advanced features: pip install svgwrite pillow numpy matplotlib")

# Color schemes for modern visual style
COLORS = {
    "primary": "#5E81F5",
    "secondary": "#41B8FF",
    "accent": "#FF5E62",
    "accent2": "#FF9966",
    "dark": "#1A1F35",
    "darker": "#141824",
    "light": "#E0E6F4",
    "muted": "#B2BEDA",
    "success": "#4CAF50",
    "warning": "#FFC107",
    "error": "#FF5252",
}

# Create directories if they don't exist
def ensure_dirs():
    """Create necessary directories if they don't exist"""
    dirs = [
        'docs/images',
        'docs/badges',
        'docs/deployment',
        'static/images/icons',
        'static/images/diagrams',
        'static/images/animations',
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


# Create modern logo with 3D cube design
def create_modern_logo(animated=False):
    """Create the modern BloxAPI logo as SVG with 3D cube effect
    
    Args:
        animated (bool): Whether to create an animated version with rotation
    """
    output_path = 'docs/images/logo.svg' if not animated else 'docs/images/logo-animated.svg'
    
    if not ADVANCED_MODE:
        print("⚠️ Advanced visualization libraries required for modern logo. Using basic logo instead.")
        return create_logo()
    
    width, height = 500, 500
    
    # Create SVG document
    dwg = svgwrite.Drawing(output_path, size=(width, height))
    
    # Create background
    dwg.add(dwg.rect((0, 0), (width, height), fill='none'))
    
    # Create a circular gradient for the background
    radial = dwg.radialGradient(center=(width/2, height/2), r=width/2)
    radial.add_stop_color(0, COLORS['primary'], 0.9)
    radial.add_stop_color(0.7, COLORS['dark'], 0.95)
    radial.add_stop_color(1, COLORS['darker'], 1)
    dwg.defs.add(radial)
    
    # Add a subtle background circle
    dwg.add(dwg.circle(center=(width/2, height/2), r=width/2.2, 
                     fill=radial.get_funciri()))
    
    # Create cube shape
    cube_size = width * 0.6
    center_x, center_y = width/2, height/2
    offset = cube_size * 0.2
    
    # Create linear gradients for each face
    top_gradient = dwg.linearGradient(start=(center_x - cube_size/2, center_y - cube_size/2), 
                                     end=(center_x, center_y - cube_size/4))
    top_gradient.add_stop_color(0, COLORS['secondary'], 0.9)
    top_gradient.add_stop_color(1, COLORS['primary'], 0.8)
    dwg.defs.add(top_gradient)
    
    left_gradient = dwg.linearGradient(start=(center_x - cube_size/2, center_y - cube_size/2), 
                                      end=(center_x - cube_size/4, center_y + cube_size/2))
    left_gradient.add_stop_color(0, COLORS['accent'], 0.9)
    left_gradient.add_stop_color(1, COLORS['accent2'], 0.8)
    dwg.defs.add(left_gradient)
    
    right_gradient = dwg.linearGradient(start=(center_x, center_y - cube_size/4), 
                                       end=(center_x + cube_size/2, center_y + cube_size/2))
    right_gradient.add_stop_color(0, COLORS['primary'], 0.95)
    right_gradient.add_stop_color(1, COLORS['dark'], 0.8)
    dwg.defs.add(right_gradient)
    
    # Draw cube faces
    # Top face (parallelogram)
    top_points = [
        (center_x - cube_size/2, center_y - cube_size/4),
        (center_x, center_y - cube_size/2),
        (center_x + cube_size/2, center_y - cube_size/4),
        (center_x, center_y),
    ]
    top_face = dwg.polygon(top_points, fill=top_gradient.get_funciri(), 
                          stroke=COLORS['light'], stroke_width=2, stroke_opacity=0.3)
    dwg.add(top_face)
    
    # Left face
    left_points = [
        (center_x - cube_size/2, center_y - cube_size/4),
        (center_x, center_y),
        (center_x, center_y + cube_size/2),
        (center_x - cube_size/2, center_y + cube_size/4),
    ]
    left_face = dwg.polygon(left_points, fill=left_gradient.get_funciri(), 
                           stroke=COLORS['light'], stroke_width=2, stroke_opacity=0.3)
    dwg.add(left_face)
    
    # Right face
    right_points = [
        (center_x, center_y),
        (center_x + cube_size/2, center_y - cube_size/4),
        (center_x + cube_size/2, center_y + cube_size/4),
        (center_x, center_y + cube_size/2),
    ]
    right_face = dwg.polygon(right_points, fill=right_gradient.get_funciri(), 
                            stroke=COLORS['light'], stroke_width=2, stroke_opacity=0.3)
    dwg.add(right_face)
    
    # Add highlights
    highlight_points = [
        (center_x - cube_size/4, center_y - cube_size/8),
        (center_x, center_y - cube_size/4),
        (center_x + cube_size/4, center_y - cube_size/8),
    ]
    dwg.add(dwg.polyline(highlight_points, stroke=COLORS['light'], 
                        stroke_width=2, stroke_opacity=0.7, fill='none'))
    
    # Add shadow beneath the cube
    shadow_filter = dwg.filter(id='shadow', x='-20%', y='-20%', width='140%', height='140%')
    shadow_filter.feGaussianBlur(in_='SourceAlpha', stdDeviation=15)
    shadow_filter.feOffset(dx=0, dy=10, result='offsetblur')
    shadow_filter.feComponentTransfer().feFuncA(type='linear', slope=0.3)
    
    filter_merge = shadow_filter.feMerge()
    filter_merge.feMergeNode(in_='offsetblur')
    filter_merge.feMergeNode(in_='SourceGraphic')
    
    dwg.defs.add(shadow_filter)
    
    # Group the cube and apply shadow
    cube_group = dwg.g(filter=shadow_filter.get_funciri())
    cube_group.add(top_face)
    cube_group.add(left_face)
    cube_group.add(right_face)
    
    # Add glow effect
    glow_filter = dwg.filter(id='glow', x='-20%', y='-20%', width='140%', height='140%')
    glow_filter.feGaussianBlur(in_='SourceAlpha', stdDeviation=10, result='blur')
    glow_filter.feFlood(flood_color=COLORS['secondary'], flood_opacity=0.3, result='color')
    glow_filter.feComposite(in_='color', in2='blur', operator='in', result='shadow')
    glow_filter.feComposite(in_='SourceGraphic', in2='shadow', operator='over')
    dwg.defs.add(glow_filter)
    
    # Apply glow to the cube
    cube_group['filter'] = glow_filter.get_funciri()
    dwg.add(cube_group)
    
    # Add animation if requested
    if animated:
        # Rotation animation
        animate = dwg.animate(
            attributeName='transform',
            type='rotate',
            from_='0 250 250',
            to='360 250 250',
            dur='20s',
            repeatCount='indefinite'
        )
        cube_group.add(animate)
        
        # Subtle pulsing animation
        animate_opacity = dwg.animate(
            attributeName='opacity',
            values='0.9;1;0.9',
            dur='3s',
            repeatCount='indefinite'
        )
        cube_group.add(animate_opacity)
    
    # Save the SVG file
    dwg.save()
    
    # Also generate PNG version for broader compatibility
    png_output_path = output_path.replace('.svg', '.png')
    try:
        subprocess.run(['rsvg-convert', '-w', '200', '-h', '200', output_path, '-o', png_output_path], check=True)
        print(f"✓ Created modern logo: {output_path} and {png_output_path}")
    except Exception as e:
        print(f"⚠️ Could not convert SVG to PNG: {e}")
        print(f"✓ Logo created at {output_path} only")
    
    return output_path

# SVG Logo Creator (basic version as fallback)
def create_logo():
    """Create the BloxAPI logo as SVG (basic version)"""
    logo_path = 'docs/images/logo.svg'
    
    # Create a simple yet attractive logo
    logo_svg = """<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#5E81F5" />
            <stop offset="100%" stop-color="#41B8FF" />
        </linearGradient>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.3" />
        </filter>
    </defs>
    <rect x="40" y="40" width="120" height="120" rx="16" fill="url(#gradient)" filter="url(#shadow)" />
    <path d="M75 70 L75 130 L90 130 L90 105 L110 105 L110 130 L125 130 L125 70 L110 70 L110 90 L90 90 L90 70 Z" 
          fill="white" />
    <circle cx="140" cy="70" r="10" fill="#FF5E62" />
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
    
    return logo_path

# Create modern feature icons with animations
def create_feature_icons():
    """Create icons for features section in README"""
    if ADVANCED_MODE:
        create_modern_feature_icons()
        return
    
    # Fallback to basic icons if advanced mode is not available
    icons = {
        'architecture': """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#5E81F5" />
                    <stop offset="100%" stop-color="#41B8FF" />
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
        
        'api-overview': """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
            <defs>
                <linearGradient id="apiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#41B8FF" />
                    <stop offset="100%" stop-color="#5E81F5" />
                </linearGradient>
            </defs>
            <rect x="10" y="10" width="80" height="80" rx="8" fill="url(#apiGrad)" />
            <path d="M30 40 L70 40 M30 60 L70 60 M40 30 L40 70 M60 30 L60 70" 
                  stroke="white" stroke-width="2" stroke-linecap="round" stroke-opacity="0.8" fill="none" />
            <circle cx="40" cy="40" r="5" fill="white" opacity="0.9" />
            <circle cx="60" cy="40" r="5" fill="white" opacity="0.9" />
            <circle cx="40" cy="60" r="5" fill="white" opacity="0.9" />
            <circle cx="60" cy="60" r="5" fill="white" opacity="0.9" />
        </svg>""",
        
        'graphql': """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
            <defs>
                <linearGradient id="graphqlGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#FF5E62" />
                    <stop offset="100%" stop-color="#FF9966" />
                </linearGradient>
            </defs>
            <rect x="10" y="10" width="80" height="80" rx="8" fill="url(#graphqlGrad)" />
            <path d="M50 25 L75 38 L75 62 L50 75 L25 62 L25 38 Z" 
                  stroke="white" stroke-width="2" stroke-opacity="0.9" fill="none" />
            <path d="M50 25 L50 75 M25 38 L75 38 M25 62 L75 62" 
                  stroke="white" stroke-width="2" stroke-opacity="0.7" fill="none" />
            <circle cx="50" cy="25" r="4" fill="white" />
            <circle cx="75" cy="38" r="4" fill="white" />
            <circle cx="75" cy="62" r="4" fill="white" />
            <circle cx="50" cy="75" r="4" fill="white" />
            <circle cx="25" cy="62" r="4" fill="white" />
            <circle cx="25" cy="38" r="4" fill="white" />
        </svg>""",
        
        'security': """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
            <defs>
                <linearGradient id="securityGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#4CAF50" />
                    <stop offset="100%" stop-color="#2E7D32" />
                </linearGradient>
            </defs>
            <rect x="10" y="10" width="80" height="80" rx="8" fill="url(#securityGrad)" />
            <path d="M50 30 L30 40 L30 60 C30 70 40 75 50 80 C60 75 70 70 70 60 L70 40 Z" 
                  fill="white" fill-opacity="0.2" stroke="white" stroke-width="2" />
            <path d="M40 55 L45 60 L60 45" 
                  stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none" />
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

# Create modern feature icons using svgwrite
def create_modern_feature_icons():
    """Create modern feature icons with advanced styling"""
    icons = [
        {"name": "api-overview", "emoji": "🔗", "title": "API Overview"},
        {"name": "architecture", "emoji": "🏗️", "title": "Architecture"},
        {"name": "code-examples", "emoji": "📝", "title": "Code Examples"},
        {"name": "documentation", "emoji": "📚", "title": "Documentation"},
        {"name": "features", "emoji": "✨", "title": "Features"},
        {"name": "installation", "emoji": "📦", "title": "Installation"},
        {"name": "security", "emoji": "🔒", "title": "Security"},
        {"name": "graphql", "emoji": "📊", "title": "GraphQL Support"},
    ]
    
    for icon in icons:
        output_svg = f"docs/images/{icon['name']}.svg"
        output_png = f"docs/images/{icon['name']}.png"
        
        # Create SVG
        width, height = 400, 250
        dwg = svgwrite.Drawing(output_svg, size=(width, height))
        
        # Background with gradient
        gradient = dwg.linearGradient(start=(0, 0), end=(width, height))
        gradient.add_stop_color(0, COLORS['dark'])
        gradient.add_stop_color(1, COLORS['darker'])
        dwg.defs.add(gradient)
        
        # Add a subtle pattern to the background
        pattern = dwg.pattern(id="pattern", patternUnits="userSpaceOnUse", size=(20, 20))
        pattern.add(dwg.rect((0, 0), (20, 20), fill=gradient.get_funciri()))
        pattern.add(dwg.circle((10, 10), r=1, fill=COLORS['primary'], fill_opacity=0.3))
        dwg.defs.add(pattern)
        
        # Add background with pattern
        dwg.add(dwg.rect((0, 0), (width, height), fill=pattern.get_funciri(), rx=10, ry=10))
        
        # Add border with primary color
        border_gradient = dwg.linearGradient(start=(0, 0), end=(width, height))
        border_gradient.add_stop_color(0, COLORS['primary'])
        border_gradient.add_stop_color(0.5, COLORS['secondary'])
        border_gradient.add_stop_color(1, COLORS['accent'])
        dwg.defs.add(border_gradient)
        
        dwg.add(dwg.rect((0, 0), (width, height), stroke=border_gradient.get_funciri(), 
                        stroke_width=2, fill='none', rx=10, ry=10))
        
        # Create a group for the icon content
        icon_group = dwg.g()
        
        # Add emoji as the central icon
        emoji_text = dwg.text(icon['emoji'], insert=(width/2, height/2-20), 
                            text_anchor="middle", font_size=80)
        icon_group.add(emoji_text)
        
        # Add title
        title_text = dwg.text(icon['title'], insert=(width/2, height/2+60), 
                             text_anchor="middle", font_size=24, 
                             fill=COLORS['light'])
        icon_group.add(title_text)
        
        # Add the icon group to the drawing
        dwg.add(icon_group)
        
        # Save the SVG
        dwg.save()
        
        # Generate PNG version
        try:
            subprocess.run(['rsvg-convert', '-w', '400', '-h', '250', output_svg, '-o', output_png], check=True)
        except Exception as e:
            print(f"⚠️ Could not convert SVG to PNG for {icon['name']}: {e}")
    
    print(f"✓ Created {len(icons)} modern feature icons in docs/images/")


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


# Create architecture diagram
def create_architecture_diagram():
    """Create an architecture diagram for the BloxAPI system"""
    if not ADVANCED_MODE:
        print("⚠️ Advanced visualization libraries required for architecture diagram.")
        return
        
    output_svg = "docs/images/api-architecture.svg"
    output_png = "docs/images/api-architecture.png"
    
    # Create SVG
    width, height = 800, 600
    dwg = svgwrite.Drawing(output_svg, size=(width, height))
    
    # Define gradients
    main_grad = dwg.linearGradient(start=(0, 0), end=(0, height))
    main_grad.add_stop_color(0, '#0F172A')
    main_grad.add_stop_color(1, '#1E293B')
    dwg.defs.add(main_grad)
    
    primary_grad = dwg.linearGradient(start=(0, 0), end=(100, 50))
    primary_grad.add_stop_color(0, COLORS['primary'])
    primary_grad.add_stop_color(1, COLORS['secondary'])
    dwg.defs.add(primary_grad)
    
    secondary_grad = dwg.linearGradient(start=(0, 0), end=(100, 50))
    secondary_grad.add_stop_color(0, COLORS['accent'])
    secondary_grad.add_stop_color(1, COLORS['accent2'])
    dwg.defs.add(secondary_grad)
    
    # Add background
    dwg.add(dwg.rect((0, 0), (width, height), fill=main_grad.get_funciri(), rx=5, ry=5))
    
    # Add grid pattern
    pattern = dwg.pattern(id="grid", patternUnits="userSpaceOnUse", size=(50, 50))
    pattern.add(dwg.path(d="M 50 0 L 0 0 0 50", fill="none", 
                        stroke=COLORS['light'], stroke_width=0.5, stroke_opacity=0.1))
    dwg.defs.add(pattern)
    
    dwg.add(dwg.rect((0, 0), (width, height), fill=pattern.get_funciri()))
    
    # Define component styles
    def create_component(x, y, w, h, title, is_primary=True, icon=None):
        group = dwg.g()
        # Create rectangle with gradient
        gradient = primary_grad if is_primary else secondary_grad
        rect = dwg.rect((x, y), (w, h), rx=10, ry=10, fill=gradient.get_funciri(),
                       stroke=COLORS['light'], stroke_width=1, stroke_opacity=0.3)
        group.add(rect)
        
        # Create inner shadow effect
        highlight = dwg.rect((x+2, y+2), (w-4, 15), rx=8, ry=8, 
                            fill='white', fill_opacity=0.15)
        group.add(highlight)
        
        # Add title
        title_text = dwg.text(title, insert=(x + w/2, y + 30), text_anchor="middle",
                             font_size=16, fill=COLORS['light'], font_weight="bold")
        group.add(title_text)
        
        # Add icon if provided
        if icon:
            icon_text = dwg.text(icon, insert=(x + w/2, y + h/2 + 10),
                               text_anchor="middle", font_size=28)
            group.add(icon_text)
            
        return group
    
    # Create connections between components
    def create_connection(start_x, start_y, end_x, end_y, is_bidirectional=False):
        marker_size = 5
        line_color = COLORS['light']
        line_opacity = 0.6
        
        # Create arrowhead marker
        marker = dwg.marker(insert=(marker_size, marker_size/2), size=(marker_size, marker_size),
                           orient="auto", markerUnits="strokeWidth")
        marker.add(dwg.path(d=f"M 0 0 L {marker_size} {marker_size/2} L 0 {marker_size} z",
                          fill=line_color))
        dwg.defs.add(marker)
        
        # Draw the path
        path = dwg.path(d=f"M {start_x} {start_y} L {end_x} {end_y}",
                       stroke=line_color, stroke_width=2, stroke_opacity=line_opacity,
                       marker_end=marker.get_funciri())
        
        # If bidirectional, add second marker
        if is_bidirectional:
            marker2 = dwg.marker(insert=(0, marker_size/2), size=(marker_size, marker_size),
                               orient="auto", markerUnits="strokeWidth")
            marker2.add(dwg.path(d=f"M {marker_size} 0 L 0 {marker_size/2} L {marker_size} {marker_size} z",
                               fill=line_color))
            dwg.defs.add(marker2)
            
            path['marker-start'] = marker2.get_funciri()
            
        return path
    
    # ************ Architecture Components ****************
    
    # Add title
    title = dwg.text("BloxAPI Architecture", insert=(width/2, 40), text_anchor="middle",
                   font_size=24, fill=COLORS['light'], font_weight="bold")
    dwg.add(title)
    
    # Add subtitle
    subtitle = dwg.text("Security-Enhanced API Integration Toolkit", insert=(width/2, 70), 
                      text_anchor="middle", font_size=16, fill=COLORS['muted'])
    dwg.add(subtitle)
    
    # Define components
    components = [
        # Core components
        {"x": 300, "y": 120, "w": 200, "h": 80, "title": "API Gateway", "is_primary": True, "icon": "🚪"},
        {"x": 300, "y": 240, "w": 200, "h": 80, "title": "GraphQL Engine", "is_primary": True, "icon": "📊"},
        {"x": 300, "y": 360, "w": 200, "h": 80, "title": "REST API Layer", "is_primary": True, "icon": "🔗"},
        {"x": 300, "y": 480, "w": 200, "h": 80, "title": "Roblox API Connector", "is_primary": True, "icon": "🎮"},
        
        # Left components
        {"x": 80, "y": 180, "w": 150, "h": 70, "title": "Bot Protection", "is_primary": False, "icon": "🤖"},
        {"x": 80, "y": 280, "w": 150, "h": 70, "title": "Fraud Detection", "is_primary": False, "icon": "🕵️"},
        {"x": 80, "y": 380, "w": 150, "h": 70, "title": "Redis Cache", "is_primary": False, "icon": "⚡"},
        
        # Right components
        {"x": 570, "y": 180, "w": 150, "h": 70, "title": "Webhooks", "is_primary": False, "icon": "🔔"},
        {"x": 570, "y": 280, "w": 150, "h": 70, "title": "Data Export", "is_primary": False, "icon": "📤"},
        {"x": 570, "y": 380, "w": 150, "h": 70, "title": "Monitoring", "is_primary": False, "icon": "📈"},
    ]
    
    # Add all components
    for comp in components:
        dwg.add(create_component(
            comp["x"], comp["y"], comp["w"], comp["h"], 
            comp["title"], comp["is_primary"], comp["icon"]
        ))
    
    # Define connections
    connections = [
        # Vertical backbone connections
        {"start_x": 400, "start_y": 200, "end_x": 400, "end_y": 240, "bidirectional": True},
        {"start_x": 400, "start_y": 320, "end_x": 400, "end_y": 360, "bidirectional": True},
        {"start_x": 400, "start_y": 440, "end_x": 400, "end_y": 480, "bidirectional": True},
        
        # Left side connections
        {"start_x": 230, "start_y": 215, "end_x": 300, "end_y": 160, "bidirectional": False},
        {"start_x": 230, "start_y": 315, "end_x": 300, "end_y": 280, "bidirectional": False},
        {"start_x": 230, "start_y": 415, "end_x": 300, "end_y": 400, "bidirectional": True},
        
        # Right side connections
        {"start_x": 500, "start_y": 160, "end_x": 570, "end_y": 215, "bidirectional": True},
        {"start_x": 500, "start_y": 280, "end_x": 570, "end_y": 315, "bidirectional": True},
        {"start_x": 500, "start_y": 400, "end_x": 570, "end_y": 415, "bidirectional": False},
    ]
    
    # Add all connections
    for conn in connections:
        dwg.add(create_connection(
            conn["start_x"], conn["start_y"], conn["end_x"], conn["end_y"], conn["bidirectional"]
        ))
    
    # Add legend
    legend_x = 50
    legend_y = 500
    legend_group = dwg.g()
    
    # Primary component legend
    legend_group.add(dwg.rect((legend_x, legend_y), (20, 20), rx=5, ry=5,
                             fill=primary_grad.get_funciri()))
    legend_group.add(dwg.text("Core Components", insert=(legend_x + 30, legend_y + 15),
                            fill=COLORS['light'], font_size=14))
    
    # Secondary component legend
    legend_group.add(dwg.rect((legend_x, legend_y + 30), (20, 20), rx=5, ry=5,
                             fill=secondary_grad.get_funciri()))
    legend_group.add(dwg.text("Security & Performance", insert=(legend_x + 30, legend_y + 45),
                            fill=COLORS['light'], font_size=14))
    
    # Add legend to diagram
    dwg.add(legend_group)
    
    # Save the SVG file
    dwg.save()
    
    # Generate PNG version
    try:
        subprocess.run(['rsvg-convert', '-w', '800', '-h', '600', output_svg, '-o', output_png], check=True)
        print(f"✓ Created architecture diagram: {output_svg} and {output_png}")
    except Exception as e:
        print(f"⚠️ Could not convert SVG to PNG: {e}")
        print(f"✓ Architecture diagram created at {output_svg} only")
    
    return output_svg

# Create API overview diagram
def create_api_overview():
    """Create visual API overview diagram"""
    if not ADVANCED_MODE:
        print("⚠️ Advanced visualization libraries required for API overview diagram.")
        return
        
    output_svg = "docs/images/api-overview.svg"
    output_png = "docs/images/api-overview.png"
    
    # Create SVG
    width, height = 900, 600
    dwg = svgwrite.Drawing(output_svg, size=(width, height))
    
    # Background
    bg_grad = dwg.linearGradient(start=(0, 0), end=(0, height))
    bg_grad.add_stop_color(0, '#0F172A')
    bg_grad.add_stop_color(1, '#1E293B')
    dwg.defs.add(bg_grad)
    dwg.add(dwg.rect((0, 0), (width, height), fill=bg_grad.get_funciri(), rx=10, ry=10))
    
    # Add subtle grid pattern
    pattern = dwg.pattern(id="grid", patternUnits="userSpaceOnUse", size=(20, 20))
    pattern.add(dwg.path(d="M 20 0 L 0 0 0 20", fill="none", 
                        stroke=COLORS['light'], stroke_width=0.2, stroke_opacity=0.1))
    dwg.defs.add(pattern)
    dwg.add(dwg.rect((0, 0), (width, height), fill=pattern.get_funciri()))
    
    # Add title
    title = dwg.text("BloxAPI Comprehensive API Coverage", insert=(width/2, 40), 
                    text_anchor="middle", font_size=28, fill=COLORS['light'], font_weight="bold")
    dwg.add(title)
    
    # Add subtitle
    subtitle = dwg.text("2000+ Integrated API Endpoints with Enhanced Security",
                       insert=(width/2, 75), text_anchor="middle", 
                       font_size=16, fill=COLORS['muted'])
    dwg.add(subtitle)
    
    # Define API categories
    categories = [
        {"name": "User Data", "icon": "👤", "count": 320, "color": "#4CAF50"},
        {"name": "Game Analysis", "icon": "🎮", "count": 280, "color": "#2196F3"},
        {"name": "Economy", "icon": "💰", "count": 210, "color": "#FFC107"},
        {"name": "Social", "icon": "👥", "count": 260, "color": "#9C27B0"},
        {"name": "Content", "icon": "🎨", "count": 320, "color": "#FF5722"},
        {"name": "Security", "icon": "🔒", "count": 180, "color": "#607D8B"},
        {"name": "Analytics", "icon": "📊", "count": 250, "color": "#3F51B5"},
        {"name": "Marketplace", "icon": "🛒", "count": 240, "color": "#E91E63"},
    ]
    
    # Create a bubble chart visualization
    center_x, center_y = width/2, height/2 + 50
    orbit_radius = 180
    max_bubble_size = 90
    min_bubble_size = 60
    
    # Calculate positions in a circle
    for i, category in enumerate(categories):
        angle = (2 * math.pi * i) / len(categories)
        x = center_x + orbit_radius * math.cos(angle)
        y = center_y + orbit_radius * math.sin(angle)
        
        # Calculate bubble size based on count
        max_count = max(cat["count"] for cat in categories)
        size_ratio = category["count"] / max_count
        bubble_size = min_bubble_size + (max_bubble_size - min_bubble_size) * size_ratio
        
        # Create gradient for bubble
        bubble_grad = dwg.radialGradient(center=(x, y), r=bubble_size/2)
        bubble_grad.add_stop_color(0, category["color"], 0.9)
        bubble_grad.add_stop_color(1, category["color"], 0.5)
        dwg.defs.add(bubble_grad)
        
        # Create bubble
        bubble = dwg.circle(center=(x, y), r=bubble_size/2, 
                          fill=bubble_grad.get_funciri(),
                          stroke=COLORS['light'], stroke_width=1, stroke_opacity=0.3)
        
        # Add glow effect
        glow = dwg.filter(id=f'glow{i}')
        glow.feGaussianBlur(in_='SourceAlpha', stdDeviation=5)
        glow.feOffset(dx=0, dy=0, result='offsetblur')
        glow.feFlood(flood_color=category["color"], flood_opacity=0.3)
        glow.feComposite(in2='offsetblur', operator='in')
        glow.feMerge().feMergeNode()
        glow.feMerge().feMergeNode(in_='SourceGraphic')
        dwg.defs.add(glow)
        
        # Apply glow to bubble
        bubble['filter'] = glow.get_funciri()
        
        # Create group for the category
        group = dwg.g()
        group.add(bubble)
        
        # Add icon
        icon = dwg.text(category["icon"], insert=(x, y-10), text_anchor="middle", font_size=32)
        group.add(icon)
        
        # Add name
        name = dwg.text(category["name"], insert=(x, y+15), text_anchor="middle", 
                       font_size=14, fill=COLORS['light'], font_weight="bold")
        group.add(name)
        
        # Add count
        count = dwg.text(f"{category['count']}+ APIs", insert=(x, y+35), text_anchor="middle", 
                        font_size=12, fill=COLORS['muted'])
        group.add(count)
        
        # Add connection to center
        line = dwg.line(start=(center_x, center_y), end=(x, y), 
                       stroke=category["color"], stroke_width=1.5, 
                       stroke_opacity=0.4, stroke_dasharray="5,3")
        dwg.add(line)
        
        # Add group to drawing
        dwg.add(group)
    
    # Create central hub
    central_grad = dwg.radialGradient(center=(center_x, center_y), r=60)
    central_grad.add_stop_color(0, COLORS['primary'], 0.9)
    central_grad.add_stop_color(1, COLORS['secondary'], 0.7)
    dwg.defs.add(central_grad)
    
    # Central hub glow
    central_glow = dwg.filter(id='central_glow')
    central_glow.feGaussianBlur(in_='SourceAlpha', stdDeviation=10)
    central_glow.feOffset(dx=0, dy=0, result='offsetblur')
    central_glow.feFlood(flood_color=COLORS['primary'], flood_opacity=0.5)
    central_glow.feComposite(in2='offsetblur', operator='in')
    central_glow.feMerge().feMergeNode()
    central_glow.feMerge().feMergeNode(in_='SourceGraphic')
    dwg.defs.add(central_glow)
    
    # Create central hub
    central_hub = dwg.circle(center=(center_x, center_y), r=60, 
                            fill=central_grad.get_funciri(),
                            stroke=COLORS['light'], stroke_width=2, stroke_opacity=0.5,
                            filter=central_glow.get_funciri())
    dwg.add(central_hub)
    
    # Add BloxAPI logo to center
    central_icon = dwg.text("🧊", insert=(center_x, center_y-10), 
                          text_anchor="middle", font_size=40)
    dwg.add(central_icon)
    
    central_text = dwg.text("BloxAPI", insert=(center_x, center_y+20), 
                          text_anchor="middle", font_size=18, fill=COLORS['light'], 
                          font_weight="bold")
    dwg.add(central_text)
    
    # Add total count
    total = sum(cat["count"] for cat in categories)
    total_text = dwg.text(f"Total: {total}+ endpoints", 
                         insert=(width/2, height-40), text_anchor="middle", 
                         font_size=16, fill=COLORS['muted'])
    dwg.add(total_text)
    
    # Save the SVG
    dwg.save()
    
    # Generate PNG version
    try:
        subprocess.run(['rsvg-convert', '-w', '900', '-h', '600', output_svg, '-o', output_png], check=True)
        print(f"✓ Created API overview: {output_svg} and {output_png}")
    except Exception as e:
        print(f"⚠️ Could not convert SVG to PNG: {e}")
        print(f"✓ API overview created at {output_svg} only")
    
    return output_svg

# Main function
def main():
    """Main function to create all assets"""
    parser = argparse.ArgumentParser(description="Generate visual assets for BloxAPI")
    parser.add_argument('--all', action='store_true', help='Generate all assets')
    parser.add_argument('--logo', action='store_true', help='Generate logo')
    parser.add_argument('--animated-logo', action='store_true', help='Generate animated logo')
    parser.add_argument('--icons', action='store_true', help='Generate feature icons')
    parser.add_argument('--architecture', action='store_true', help='Generate architecture diagram')
    parser.add_argument('--api-overview', action='store_true', help='Generate API overview diagram')
    parser.add_argument('--deployment', action='store_true', help='Generate deployment docs')
    
    args = parser.parse_args()
    
    # If no specific options, generate all
    if not (args.logo or args.animated_logo or args.icons or args.architecture or args.api_overview or args.deployment):
        args.all = True
    
    print(f"🎨 BloxAPI Visual Asset Generator")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    ensure_dirs()
    
    if args.all or args.logo:
        try:
            if ADVANCED_MODE:
                create_modern_logo()
            else:
                create_logo()
        except Exception as e:
            print(f"⚠️ Error creating logo: {e}")
            create_logo()  # Fallback to basic version
    
    if args.all or args.animated_logo:
        try:
            if ADVANCED_MODE:
                create_modern_logo(animated=True)
        except Exception as e:
            print(f"⚠️ Error creating animated logo: {e}")
    
    if args.all or args.icons:
        create_feature_icons()
    
    if args.all or args.architecture:
        create_architecture_diagram()
    
    if args.all or args.api_overview:
        create_api_overview()
    
    if args.all or args.deployment:
        create_deployment_docs()
    
    print("\n✅ All README assets created successfully!")


if __name__ == "__main__":
    main()