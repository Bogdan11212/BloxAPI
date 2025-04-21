"""
Data Migration Utilities for BloxAPI

This module provides functionality for migrating data between games
and exporting/importing game data for backup or transfer.
"""

import os
import json
import logging
import time
import zipfile
import tempfile
import hashlib
from typing import Dict, List, Any, Optional, Union, Callable, Set
from datetime import datetime
import io
import base64
import csv
from .roblox_api import RobloxAPI

# Configure logging
logger = logging.getLogger(__name__)

class MigrationError(Exception):
    """Exception raised for errors during migration"""
    pass

class DataExporter:
    """
    Class for exporting game data for backup or migration
    """
    
    def __init__(self, api: Optional[RobloxAPI] = None):
        """
        Initialize the data exporter
        
        Args:
            api: RobloxAPI instance
        """
        self.api = api or RobloxAPI()
    
    def export_game(self, universe_id: int, export_options: Dict[str, bool] = None) -> io.BytesIO:
        """
        Export game data to a zip file
        
        Args:
            universe_id: Universe ID of the game
            export_options: Dictionary of data types to export
                Possible keys:
                - badges: Export game badges
                - game_passes: Export game passes
                - developer_products: Export developer products
                - places: Export place data
                - social_links: Export social links
                - icon: Export game icon
                - thumbnails: Export game thumbnails
                - revenue: Export revenue data (requires additional permissions)
                - analytics: Export analytics data (requires additional permissions)
                
        Returns:
            BytesIO object containing the zip file
        """
        # Default export options
        if export_options is None:
            export_options = {
                "badges": True,
                "game_passes": True,
                "developer_products": True,
                "places": True,
                "social_links": True,
                "icon": True,
                "thumbnails": True,
                "revenue": False,
                "analytics": False
            }
        
        # Get basic game data
        try:
            game_data = self.api.games.get_game_details(universe_id)
            if not game_data:
                raise MigrationError(f"Game with universe ID {universe_id} not found")
        except Exception as e:
            raise MigrationError(f"Failed to get game data: {str(e)}")
        
        # Create in-memory zip file
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add game info
            zipf.writestr("game_info.json", json.dumps(game_data, indent=2))
            
            # Add metadata about the export
            metadata = {
                "export_date": datetime.now().isoformat(),
                "universe_id": universe_id,
                "export_options": export_options,
                "bloxapi_version": "2.0.0"  # TODO: Get version dynamically
            }
            zipf.writestr("metadata.json", json.dumps(metadata, indent=2))
            
            # Export badges
            if export_options.get("badges", False):
                self._export_badges(zipf, universe_id)
            
            # Export game passes
            if export_options.get("game_passes", False):
                self._export_game_passes(zipf, universe_id)
            
            # Export developer products
            if export_options.get("developer_products", False):
                self._export_developer_products(zipf, universe_id)
            
            # Export places
            if export_options.get("places", False):
                self._export_places(zipf, universe_id)
            
            # Export social links
            if export_options.get("social_links", False):
                self._export_social_links(zipf, universe_id)
            
            # Export game icon
            if export_options.get("icon", False):
                self._export_game_icon(zipf, universe_id)
            
            # Export thumbnails
            if export_options.get("thumbnails", False):
                self._export_thumbnails(zipf, universe_id)
            
            # Export revenue data
            if export_options.get("revenue", False):
                self._export_revenue(zipf, universe_id)
            
            # Export analytics data
            if export_options.get("analytics", False):
                self._export_analytics(zipf, universe_id)
        
        # Reset buffer position
        zip_buffer.seek(0)
        return zip_buffer
    
    def _export_badges(self, zipf: zipfile.ZipFile, universe_id: int) -> None:
        """Export badges for a game"""
        try:
            badges = self.api.badges.get_game_badges(universe_id)
            
            if badges:
                zipf.writestr("badges/badges.json", json.dumps(badges, indent=2))
                
                # Export badge icons
                os.makedirs("temp_icons", exist_ok=True)
                
                for badge in badges.get("data", []):
                    badge_id = badge.get("id")
                    
                    if badge_id:
                        try:
                            # Get badge icon
                            icon_data = self.api.badges.get_badge_icon(badge_id)
                            
                            if icon_data:
                                zipf.writestr(f"badges/icons/{badge_id}.png", icon_data)
                        except Exception as e:
                            logger.warning(f"Failed to export badge icon for badge {badge_id}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Failed to export badges: {str(e)}")
    
    def _export_game_passes(self, zipf: zipfile.ZipFile, universe_id: int) -> None:
        """Export game passes for a game"""
        try:
            game_passes = self.api.games.get_game_passes(universe_id)
            
            if game_passes:
                zipf.writestr("game_passes/game_passes.json", json.dumps(game_passes, indent=2))
                
                # Export game pass icons
                for game_pass in game_passes.get("data", []):
                    game_pass_id = game_pass.get("id")
                    
                    if game_pass_id:
                        try:
                            # Get game pass icon
                            icon_data = self.api.games.get_game_pass_icon(game_pass_id)
                            
                            if icon_data:
                                zipf.writestr(f"game_passes/icons/{game_pass_id}.png", icon_data)
                        except Exception as e:
                            logger.warning(f"Failed to export game pass icon for game pass {game_pass_id}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Failed to export game passes: {str(e)}")
    
    def _export_developer_products(self, zipf: zipfile.ZipFile, universe_id: int) -> None:
        """Export developer products for a game"""
        try:
            developer_products = self.api.games.get_developer_products(universe_id)
            
            if developer_products:
                zipf.writestr("developer_products/developer_products.json", 
                            json.dumps(developer_products, indent=2))
        
        except Exception as e:
            logger.error(f"Failed to export developer products: {str(e)}")
    
    def _export_places(self, zipf: zipfile.ZipFile, universe_id: int) -> None:
        """Export place data for a game"""
        try:
            places = self.api.games.get_game_places(universe_id)
            
            if places:
                zipf.writestr("places/places.json", json.dumps(places, indent=2))
                
                # Export place details
                for place in places.get("data", []):
                    place_id = place.get("id")
                    
                    if place_id:
                        try:
                            # Get place details
                            place_details = self.api.games.get_place_details(place_id)
                            
                            if place_details:
                                zipf.writestr(f"places/details/{place_id}.json", 
                                            json.dumps(place_details, indent=2))
                        except Exception as e:
                            logger.warning(f"Failed to export place details for place {place_id}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Failed to export places: {str(e)}")
    
    def _export_social_links(self, zipf: zipfile.ZipFile, universe_id: int) -> None:
        """Export social links for a game"""
        try:
            social_links = self.api.games.get_game_social_links(universe_id)
            
            if social_links:
                zipf.writestr("social_links/social_links.json", 
                            json.dumps(social_links, indent=2))
        
        except Exception as e:
            logger.error(f"Failed to export social links: {str(e)}")
    
    def _export_game_icon(self, zipf: zipfile.ZipFile, universe_id: int) -> None:
        """Export game icon"""
        try:
            icon_data = self.api.games.get_game_icon(universe_id)
            
            if icon_data:
                zipf.writestr("icons/game_icon.png", icon_data)
        
        except Exception as e:
            logger.error(f"Failed to export game icon: {str(e)}")
    
    def _export_thumbnails(self, zipf: zipfile.ZipFile, universe_id: int) -> None:
        """Export game thumbnails"""
        try:
            thumbnails = self.api.games.get_game_thumbnails(universe_id)
            
            if thumbnails:
                zipf.writestr("thumbnails/thumbnails.json", 
                            json.dumps(thumbnails, indent=2))
                
                # Export thumbnail images
                for i, thumbnail in enumerate(thumbnails.get("data", [])):
                    thumbnail_url = thumbnail.get("url")
                    
                    if thumbnail_url:
                        try:
                            # Download thumbnail
                            thumbnail_data = self.api.download_image(thumbnail_url)
                            
                            if thumbnail_data:
                                zipf.writestr(f"thumbnails/images/thumbnail_{i+1}.png", 
                                            thumbnail_data)
                        except Exception as e:
                            logger.warning(f"Failed to export thumbnail {i+1}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Failed to export thumbnails: {str(e)}")
    
    def _export_revenue(self, zipf: zipfile.ZipFile, universe_id: int) -> None:
        """Export revenue data for a game"""
        try:
            # Check if we have permission to access revenue data
            if not self.api.has_permission(f"universe:{universe_id}:revenue:read"):
                logger.warning("No permission to access revenue data")
                return
            
            # Get revenue summary
            revenue_summary = self.api.games.get_revenue_summary(universe_id)
            
            if revenue_summary:
                zipf.writestr("revenue/revenue_summary.json", 
                            json.dumps(revenue_summary, indent=2))
            
            # Get detailed revenue data
            # Note: This might be rate-limited or require additional permissions
            try:
                end_date = datetime.now()
                start_date = end_date.replace(year=end_date.year - 1)  # Last year of data
                
                revenue_details = self.api.games.get_revenue_details(
                    universe_id,
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d")
                )
                
                if revenue_details:
                    zipf.writestr("revenue/revenue_details.json", 
                                json.dumps(revenue_details, indent=2))
            
            except Exception as e:
                logger.warning(f"Failed to export detailed revenue data: {str(e)}")
        
        except Exception as e:
            logger.error(f"Failed to export revenue data: {str(e)}")
    
    def _export_analytics(self, zipf: zipfile.ZipFile, universe_id: int) -> None:
        """Export analytics data for a game"""
        try:
            # Check if we have permission to access analytics data
            if not self.api.has_permission(f"universe:{universe_id}:analytics:read"):
                logger.warning("No permission to access analytics data")
                return
            
            # Export different analytics metrics
            metrics = [
                "visits", "concurrent", "playtime",
                "new_players", "retention", "device_types"
            ]
            
            for metric in metrics:
                try:
                    # Get analytics for the metric
                    analytics_data = self.api.analytics.get_game_analytics(
                        universe_id, 
                        metric_type=metric,
                        time_frame="past30days"
                    )
                    
                    if analytics_data:
                        zipf.writestr(f"analytics/{metric}.json", 
                                    json.dumps(analytics_data, indent=2))
                
                except Exception as e:
                    logger.warning(f"Failed to export analytics for {metric}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Failed to export analytics data: {str(e)}")


class DataImporter:
    """
    Class for importing game data from a backup or for migration
    """
    
    def __init__(self, api: Optional[RobloxAPI] = None):
        """
        Initialize the data importer
        
        Args:
            api: RobloxAPI instance
        """
        self.api = api or RobloxAPI()
    
    def import_game(self, universe_id: int, import_data: Union[io.BytesIO, str, bytes],
                  import_options: Dict[str, bool] = None) -> Dict[str, Any]:
        """
        Import game data from a zip file
        
        Args:
            universe_id: Target universe ID to import into
            import_data: Zip file data (BytesIO, filename, or bytes)
            import_options: Dictionary of data types to import
                Possible keys:
                - badges: Import game badges
                - game_passes: Import game passes
                - developer_products: Import developer products
                - places: Import place data
                - social_links: Import social links
                - icon: Import game icon
                - thumbnails: Import game thumbnails
                
        Returns:
            Dictionary with import results
        """
        # Default import options
        if import_options is None:
            import_options = {
                "badges": True,
                "game_passes": True,
                "developer_products": True,
                "places": False,  # Places might require special handling
                "social_links": True,
                "icon": True,
                "thumbnails": True
            }
        
        # Validation
        try:
            # Check if target game exists
            game_data = self.api.games.get_game_details(universe_id)
            if not game_data:
                raise MigrationError(f"Target game with universe ID {universe_id} not found")
            
            # Check if we have permissions to update the game
            if not self.api.has_permission(f"universe:{universe_id}:update"):
                raise MigrationError(f"No permission to update game with universe ID {universe_id}")
        except Exception as e:
            raise MigrationError(f"Validation failed: {str(e)}")
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Open zip file
            if isinstance(import_data, io.BytesIO):
                zip_file = import_data
            elif isinstance(import_data, str):
                # Assume it's a filename
                if not os.path.exists(import_data):
                    raise MigrationError(f"Import file not found: {import_data}")
                zip_file = open(import_data, 'rb')
            else:
                # Assume it's bytes
                zip_file = io.BytesIO(import_data)
            
            # Extract zip contents
            with zipfile.ZipFile(zip_file) as zipf:
                zipf.extractall(temp_dir)
            
            # Close the file if it's an open file
            if isinstance(import_data, str):
                zip_file.close()
            
            # Load metadata
            try:
                with open(os.path.join(temp_dir, "metadata.json"), 'r') as f:
                    metadata = json.load(f)
                
                source_universe_id = metadata.get("universe_id")
                if not source_universe_id:
                    raise MigrationError("Source universe ID not found in metadata")
                
                # Check if source and target are the same
                if source_universe_id == universe_id:
                    logger.warning("Source and target universe IDs are the same")
            except Exception as e:
                raise MigrationError(f"Failed to load metadata: {str(e)}")
            
            # Import data
            results = {
                "status": "success",
                "source_universe_id": source_universe_id,
                "target_universe_id": universe_id,
                "imported_items": {}
            }
            
            # Import badges
            if import_options.get("badges", False):
                badge_results = self._import_badges(temp_dir, universe_id)
                results["imported_items"]["badges"] = badge_results
            
            # Import game passes
            if import_options.get("game_passes", False):
                game_pass_results = self._import_game_passes(temp_dir, universe_id)
                results["imported_items"]["game_passes"] = game_pass_results
            
            # Import developer products
            if import_options.get("developer_products", False):
                product_results = self._import_developer_products(temp_dir, universe_id)
                results["imported_items"]["developer_products"] = product_results
            
            # Import places (requires special handling)
            if import_options.get("places", False):
                place_results = self._import_places(temp_dir, universe_id)
                results["imported_items"]["places"] = place_results
            
            # Import social links
            if import_options.get("social_links", False):
                social_link_results = self._import_social_links(temp_dir, universe_id)
                results["imported_items"]["social_links"] = social_link_results
            
            # Import game icon
            if import_options.get("icon", False):
                icon_result = self._import_game_icon(temp_dir, universe_id)
                results["imported_items"]["icon"] = icon_result
            
            # Import thumbnails
            if import_options.get("thumbnails", False):
                thumbnail_results = self._import_thumbnails(temp_dir, universe_id)
                results["imported_items"]["thumbnails"] = thumbnail_results
            
            return results
    
    def _import_badges(self, temp_dir: str, universe_id: int) -> Dict[str, Any]:
        """Import badges into a game"""
        results = {
            "success": True,
            "created": 0,
            "errors": []
        }
        
        try:
            # Load badge data
            badges_file = os.path.join(temp_dir, "badges/badges.json")
            
            if not os.path.exists(badges_file):
                results["success"] = False
                results["errors"].append("Badges data not found")
                return results
            
            with open(badges_file, 'r') as f:
                badges_data = json.load(f)
            
            # Process each badge
            for badge in badges_data.get("data", []):
                try:
                    # Extract badge details
                    name = badge.get("name")
                    description = badge.get("description")
                    enabled = badge.get("enabled", True)
                    
                    # Load badge icon
                    badge_id = badge.get("id")
                    icon_path = os.path.join(temp_dir, f"badges/icons/{badge_id}.png")
                    icon_data = None
                    
                    if os.path.exists(icon_path):
                        with open(icon_path, 'rb') as icon_file:
                            icon_data = icon_file.read()
                    
                    # Create badge in target game
                    if name and description:
                        create_result = self.api.badges.create_badge(
                            universe_id=universe_id,
                            name=name,
                            description=description,
                            enabled=enabled,
                            icon_data=icon_data
                        )
                        
                        if create_result and create_result.get("id"):
                            results["created"] += 1
                        else:
                            results["errors"].append(f"Failed to create badge: {name}")
                    else:
                        results["errors"].append(f"Invalid badge data: missing name or description")
                
                except Exception as e:
                    results["errors"].append(f"Error processing badge: {str(e)}")
            
            # Update success flag if any errors
            if results["errors"]:
                results["success"] = False
        
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Failed to import badges: {str(e)}")
        
        return results
    
    def _import_game_passes(self, temp_dir: str, universe_id: int) -> Dict[str, Any]:
        """Import game passes into a game"""
        results = {
            "success": True,
            "created": 0,
            "errors": []
        }
        
        try:
            # Load game pass data
            game_passes_file = os.path.join(temp_dir, "game_passes/game_passes.json")
            
            if not os.path.exists(game_passes_file):
                results["success"] = False
                results["errors"].append("Game passes data not found")
                return results
            
            with open(game_passes_file, 'r') as f:
                game_passes_data = json.load(f)
            
            # Process each game pass
            for game_pass in game_passes_data.get("data", []):
                try:
                    # Extract game pass details
                    name = game_pass.get("name")
                    description = game_pass.get("description")
                    price = game_pass.get("price", 0)
                    
                    # Load game pass icon
                    game_pass_id = game_pass.get("id")
                    icon_path = os.path.join(temp_dir, f"game_passes/icons/{game_pass_id}.png")
                    icon_data = None
                    
                    if os.path.exists(icon_path):
                        with open(icon_path, 'rb') as icon_file:
                            icon_data = icon_file.read()
                    
                    # Create game pass in target game
                    if name and description is not None:
                        create_result = self.api.games.create_game_pass(
                            universe_id=universe_id,
                            name=name,
                            description=description,
                            price=price,
                            icon_data=icon_data
                        )
                        
                        if create_result and create_result.get("id"):
                            results["created"] += 1
                        else:
                            results["errors"].append(f"Failed to create game pass: {name}")
                    else:
                        results["errors"].append(f"Invalid game pass data: missing name or description")
                
                except Exception as e:
                    results["errors"].append(f"Error processing game pass: {str(e)}")
            
            # Update success flag if any errors
            if results["errors"]:
                results["success"] = False
        
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Failed to import game passes: {str(e)}")
        
        return results
    
    def _import_developer_products(self, temp_dir: str, universe_id: int) -> Dict[str, Any]:
        """Import developer products into a game"""
        results = {
            "success": True,
            "created": 0,
            "errors": []
        }
        
        try:
            # Load developer products data
            products_file = os.path.join(temp_dir, "developer_products/developer_products.json")
            
            if not os.path.exists(products_file):
                results["success"] = False
                results["errors"].append("Developer products data not found")
                return results
            
            with open(products_file, 'r') as f:
                products_data = json.load(f)
            
            # Process each developer product
            for product in products_data.get("data", []):
                try:
                    # Extract product details
                    name = product.get("name")
                    description = product.get("description")
                    price = product.get("price", 0)
                    
                    # Create developer product in target game
                    if name:
                        create_result = self.api.games.create_developer_product(
                            universe_id=universe_id,
                            name=name,
                            description=description,
                            price=price
                        )
                        
                        if create_result and create_result.get("id"):
                            results["created"] += 1
                        else:
                            results["errors"].append(f"Failed to create developer product: {name}")
                    else:
                        results["errors"].append(f"Invalid developer product data: missing name")
                
                except Exception as e:
                    results["errors"].append(f"Error processing developer product: {str(e)}")
            
            # Update success flag if any errors
            if results["errors"]:
                results["success"] = False
        
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Failed to import developer products: {str(e)}")
        
        return results
    
    def _import_places(self, temp_dir: str, universe_id: int) -> Dict[str, Any]:
        """Import place data into a game (limited functionality)"""
        results = {
            "success": True,
            "updated": 0,
            "errors": []
        }
        
        try:
            # Note: Full place importing is limited by API restrictions
            # We can only update place configuration, not actual place files
            
            # Load places data
            places_file = os.path.join(temp_dir, "places/places.json")
            
            if not os.path.exists(places_file):
                results["success"] = False
                results["errors"].append("Places data not found")
                return results
            
            with open(places_file, 'r') as f:
                places_data = json.load(f)
            
            # Get existing places in target game
            target_places = self.api.games.get_game_places(universe_id)
            if not target_places or not target_places.get("data"):
                results["success"] = False
                results["errors"].append("No places found in target game")
                return results
            
            # Process each place
            for place_index, place in enumerate(places_data.get("data", [])):
                try:
                    # Get source place details
                    place_id = place.get("id")
                    place_detail_file = os.path.join(temp_dir, f"places/details/{place_id}.json")
                    
                    if os.path.exists(place_detail_file):
                        with open(place_detail_file, 'r') as f:
                            place_details = json.load(f)
                        
                        # Get corresponding target place (by index or name)
                        target_place = None
                        if place_index < len(target_places.get("data", [])):
                            target_place = target_places["data"][place_index]
                        else:
                            # Try to find by name
                            for tp in target_places.get("data", []):
                                if tp.get("name") == place.get("name"):
                                    target_place = tp
                                    break
                        
                        if target_place:
                            target_place_id = target_place.get("id")
                            
                            # Update place configuration (name, description, etc.)
                            update_result = self.api.games.update_place_configuration(
                                place_id=target_place_id,
                                name=place_details.get("name"),
                                description=place_details.get("description")
                                # Add other configuration options as needed
                            )
                            
                            if update_result:
                                results["updated"] += 1
                            else:
                                results["errors"].append(f"Failed to update place: {place.get('name')}")
                        else:
                            results["errors"].append(f"No matching target place for: {place.get('name')}")
                    else:
                        results["errors"].append(f"Place details not found for place ID: {place_id}")
                
                except Exception as e:
                    results["errors"].append(f"Error processing place: {str(e)}")
            
            # Update success flag if any errors
            if results["errors"]:
                results["success"] = False
        
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Failed to import places: {str(e)}")
        
        return results
    
    def _import_social_links(self, temp_dir: str, universe_id: int) -> Dict[str, Any]:
        """Import social links into a game"""
        results = {
            "success": True,
            "updated": 0,
            "errors": []
        }
        
        try:
            # Load social links data
            links_file = os.path.join(temp_dir, "social_links/social_links.json")
            
            if not os.path.exists(links_file):
                results["success"] = False
                results["errors"].append("Social links data not found")
                return results
            
            with open(links_file, 'r') as f:
                links_data = json.load(f)
            
            # Process social links
            for link in links_data.get("data", []):
                try:
                    # Extract link details
                    type_name = link.get("type")
                    url = link.get("url")
                    title = link.get("title")
                    
                    if type_name and url:
                        # Add or update social link
                        update_result = self.api.games.add_social_link(
                            universe_id=universe_id,
                            type_name=type_name,
                            url=url,
                            title=title
                        )
                        
                        if update_result:
                            results["updated"] += 1
                        else:
                            results["errors"].append(f"Failed to add social link: {type_name}")
                    else:
                        results["errors"].append(f"Invalid social link data: missing type or URL")
                
                except Exception as e:
                    results["errors"].append(f"Error processing social link: {str(e)}")
            
            # Update success flag if any errors
            if results["errors"]:
                results["success"] = False
        
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Failed to import social links: {str(e)}")
        
        return results
    
    def _import_game_icon(self, temp_dir: str, universe_id: int) -> Dict[str, Any]:
        """Import game icon"""
        results = {
            "success": True,
            "updated": False,
            "errors": []
        }
        
        try:
            # Load game icon
            icon_path = os.path.join(temp_dir, "icons/game_icon.png")
            
            if not os.path.exists(icon_path):
                results["success"] = False
                results["errors"].append("Game icon file not found")
                return results
            
            with open(icon_path, 'rb') as f:
                icon_data = f.read()
            
            # Update game icon
            update_result = self.api.games.update_game_icon(
                universe_id=universe_id,
                icon_data=icon_data
            )
            
            if update_result:
                results["updated"] = True
            else:
                results["success"] = False
                results["errors"].append("Failed to update game icon")
        
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Failed to import game icon: {str(e)}")
        
        return results
    
    def _import_thumbnails(self, temp_dir: str, universe_id: int) -> Dict[str, Any]:
        """Import game thumbnails"""
        results = {
            "success": True,
            "updated": 0,
            "errors": []
        }
        
        try:
            # Get list of thumbnail files
            thumbnails_dir = os.path.join(temp_dir, "thumbnails/images")
            
            if not os.path.exists(thumbnails_dir):
                results["success"] = False
                results["errors"].append("Thumbnails directory not found")
                return results
            
            # Get list of thumbnail files
            thumbnail_files = [f for f in os.listdir(thumbnails_dir) 
                             if f.endswith('.png') or f.endswith('.jpg')]
            
            if not thumbnail_files:
                results["success"] = False
                results["errors"].append("No thumbnail files found")
                return results
            
            # Upload thumbnails
            for thumbnail_file in thumbnail_files:
                try:
                    file_path = os.path.join(thumbnails_dir, thumbnail_file)
                    
                    with open(file_path, 'rb') as f:
                        thumbnail_data = f.read()
                    
                    # Upload thumbnail
                    upload_result = self.api.games.upload_game_thumbnail(
                        universe_id=universe_id,
                        thumbnail_data=thumbnail_data
                    )
                    
                    if upload_result:
                        results["updated"] += 1
                    else:
                        results["errors"].append(f"Failed to upload thumbnail: {thumbnail_file}")
                
                except Exception as e:
                    results["errors"].append(f"Error processing thumbnail {thumbnail_file}: {str(e)}")
            
            # Update success flag if any errors
            if results["errors"]:
                results["success"] = False
        
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Failed to import thumbnails: {str(e)}")
        
        return results


class GameMigrator:
    """
    High-level class for migrating data between games
    """
    
    def __init__(self, api: Optional[RobloxAPI] = None):
        """
        Initialize the game migrator
        
        Args:
            api: RobloxAPI instance
        """
        self.api = api or RobloxAPI()
        self.exporter = DataExporter(self.api)
        self.importer = DataImporter(self.api)
    
    def migrate_game(self, source_universe_id: int, target_universe_id: int,
                   migration_options: Dict[str, bool] = None) -> Dict[str, Any]:
        """
        Migrate data from one game to another
        
        Args:
            source_universe_id: Source universe ID
            target_universe_id: Target universe ID
            migration_options: Dictionary of data types to migrate
                
        Returns:
            Dictionary with migration results
        """
        # Default migration options
        if migration_options is None:
            migration_options = {
                "badges": True,
                "game_passes": True,
                "developer_products": True,
                "places": False,  # Places might require special handling
                "social_links": True,
                "icon": True,
                "thumbnails": True
            }
        
        # Validate source and target games
        try:
            # Check if source game exists
            source_game = self.api.games.get_game_details(source_universe_id)
            if not source_game:
                raise MigrationError(f"Source game with universe ID {source_universe_id} not found")
            
            # Check if target game exists
            target_game = self.api.games.get_game_details(target_universe_id)
            if not target_game:
                raise MigrationError(f"Target game with universe ID {target_universe_id} not found")
            
            # Check if we have permissions for both games
            if not self.api.has_permission(f"universe:{source_universe_id}:read"):
                raise MigrationError(f"No permission to read from game with universe ID {source_universe_id}")
            
            if not self.api.has_permission(f"universe:{target_universe_id}:update"):
                raise MigrationError(f"No permission to update game with universe ID {target_universe_id}")
        
        except Exception as e:
            raise MigrationError(f"Validation failed: {str(e)}")
        
        # Export data from source game
        try:
            logger.info(f"Exporting data from game {source_universe_id}")
            export_data = self.exporter.export_game(source_universe_id, migration_options)
        except Exception as e:
            raise MigrationError(f"Export failed: {str(e)}")
        
        # Import data to target game
        try:
            logger.info(f"Importing data to game {target_universe_id}")
            import_results = self.importer.import_game(
                target_universe_id, 
                export_data,
                migration_options
            )
            
            # Add migration metadata
            import_results["migration"] = {
                "source_game": {
                    "universe_id": source_universe_id,
                    "name": source_game.get("name"),
                    "creator": source_game.get("creator", {}).get("name")
                },
                "target_game": {
                    "universe_id": target_universe_id,
                    "name": target_game.get("name"),
                    "creator": target_game.get("creator", {}).get("name")
                },
                "migration_date": datetime.now().isoformat(),
                "migration_options": migration_options
            }
            
            return import_results
        
        except Exception as e:
            raise MigrationError(f"Import failed: {str(e)}")


# Helper functions

def export_game_data(universe_id: int, filename: Optional[str] = None,
                    export_options: Dict[str, bool] = None) -> Union[str, io.BytesIO]:
    """
    Export game data to a file or BytesIO object
    
    Args:
        universe_id: Universe ID of the game
        filename: Output filename (if not provided, returns BytesIO object)
        export_options: Dictionary of data types to export
            
    Returns:
        Filename if filename provided, otherwise BytesIO object
    """
    exporter = DataExporter()
    data = exporter.export_game(universe_id, export_options)
    
    if filename:
        # Ensure the filename has .zip extension
        if not filename.lower().endswith('.zip'):
            filename += '.zip'
        
        # Write to file
        with open(filename, 'wb') as f:
            f.write(data.getvalue())
        
        return filename
    
    return data

def import_game_data(universe_id: int, import_data: Union[io.BytesIO, str, bytes],
                    import_options: Dict[str, bool] = None) -> Dict[str, Any]:
    """
    Import game data from a file or BytesIO object
    
    Args:
        universe_id: Target universe ID to import into
        import_data: Zip file data (BytesIO, filename, or bytes)
        import_options: Dictionary of data types to import
            
    Returns:
        Dictionary with import results
    """
    importer = DataImporter()
    return importer.import_game(universe_id, import_data, import_options)

def migrate_game(source_universe_id: int, target_universe_id: int,
               migration_options: Dict[str, bool] = None) -> Dict[str, Any]:
    """
    Migrate data from one game to another
    
    Args:
        source_universe_id: Source universe ID
        target_universe_id: Target universe ID
        migration_options: Dictionary of data types to migrate
            
    Returns:
        Dictionary with migration results
    """
    migrator = GameMigrator()
    return migrator.migrate_game(source_universe_id, target_universe_id, migration_options)