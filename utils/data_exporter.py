"""
Data Exporter for BloxAPI

This module provides functionality for exporting data in various formats,
including CSV, JSON, and XML. It can handle complex data structures and
provides customization options for the export format.
"""

import csv
import json
import logging
import io
import os
import zipfile
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

# Configure logging
logger = logging.getLogger(__name__)

class DataExporter:
    """
    Class for exporting data in various formats.
    """
    
    FORMATS = ["csv", "json", "xml", "excel"]
    
    def __init__(self, prettify: bool = True):
        """
        Initialize the data exporter.
        
        Args:
            prettify: Whether to prettify the output (where applicable)
        """
        self.prettify = prettify
    
    def export(self, data: Union[List[Dict[str, Any]], Dict[str, Any]],
               format: str, filename: Optional[str] = None,
               **options) -> Union[str, bytes]:
        """
        Export data to the specified format.
        
        Args:
            data: Data to export (list of dictionaries or a dictionary)
            format: Export format (csv, json, xml, excel)
            filename: Output filename (if not provided, returns the content)
            **options: Format-specific options
            
        Returns:
            File content as string or bytes if no filename is provided,
            otherwise returns the output filename
        """
        format = format.lower()
        
        if format not in self.FORMATS:
            raise ValueError(f"Unsupported format: {format}. "
                           f"Supported formats: {', '.join(self.FORMATS)}")
        
        # Export to the specified format
        if format == "csv":
            result = self._export_csv(data, **options)
        elif format == "json":
            result = self._export_json(data, **options)
        elif format == "xml":
            result = self._export_xml(data, **options)
        elif format == "excel":
            result = self._export_excel(data, **options)
        
        # Save to file if filename is provided
        if filename:
            output_filename = self._ensure_extension(filename, format)
            
            # Determine write mode
            mode = "wb" if isinstance(result, bytes) else "w"
            encoding = None if isinstance(result, bytes) else "utf-8"
            
            with open(output_filename, mode, encoding=encoding) as f:
                f.write(result)
            
            logger.info(f"Exported data to {output_filename}")
            return output_filename
        
        return result
    
    def _export_csv(self, data: Union[List[Dict[str, Any]], Dict[str, Any]],
                   dialect: str = "excel", delimiter: str = ",",
                   quotechar: str = '"', **options) -> str:
        """
        Export data to CSV format.
        
        Args:
            data: Data to export
            dialect: CSV dialect
            delimiter: Field delimiter
            quotechar: Quote character
            **options: Additional options
            
        Returns:
            CSV content as string
        """
        # Ensure data is a list of dictionaries
        if isinstance(data, dict):
            data = [data]
        
        # Handle empty data
        if not data:
            return ""
        
        # Extract field names from the first item
        fieldnames = list(data[0].keys())
        
        # Update fieldnames with any missing keys from other items
        for item in data[1:]:
            for key in item.keys():
                if key not in fieldnames:
                    fieldnames.append(key)
        
        # Create CSV output
        output = io.StringIO()
        writer = csv.DictWriter(
            output, fieldnames=fieldnames,
            dialect=dialect, delimiter=delimiter,
            quotechar=quotechar, quoting=csv.QUOTE_MINIMAL
        )
        
        # Write header
        writer.writeheader()
        
        # Write data
        for item in data:
            # Handle nested structures
            flat_item = self._flatten_dict(item)
            writer.writerow(flat_item)
        
        return output.getvalue()
    
    def _export_json(self, data: Union[List[Dict[str, Any]], Dict[str, Any]],
                    indent: Optional[int] = None, **options) -> str:
        """
        Export data to JSON format.
        
        Args:
            data: Data to export
            indent: Indentation level (None for compact JSON)
            **options: Additional options
            
        Returns:
            JSON content as string
        """
        # Use indentation if prettify is enabled
        indent = 2 if self.prettify and indent is None else indent
        
        # Convert datetime objects to ISO format
        return json.dumps(data, default=self._json_serializer,
                         indent=indent, ensure_ascii=False)
    
    def _export_xml(self, data: Union[List[Dict[str, Any]], Dict[str, Any]],
                   root_tag: str = "data", item_tag: str = "item",
                   **options) -> str:
        """
        Export data to XML format.
        
        Args:
            data: Data to export
            root_tag: Name of the root XML element
            item_tag: Name of the item XML elements (for lists)
            **options: Additional options
            
        Returns:
            XML content as string
        """
        # Create root element
        root = ET.Element(root_tag)
        
        # Add data to XML tree
        if isinstance(data, list):
            for item in data:
                item_element = ET.SubElement(root, item_tag)
                self._dict_to_xml(item, item_element)
        else:
            self._dict_to_xml(data, root)
        
        # Convert to string
        xml_str = ET.tostring(root, encoding="unicode")
        
        # Prettify if enabled
        if self.prettify:
            xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
        
        return xml_str
    
    def _export_excel(self, data: Union[List[Dict[str, Any]], Dict[str, Any]],
                     sheet_name: str = "Data", **options) -> bytes:
        """
        Export data to Excel format.
        
        Args:
            data: Data to export
            sheet_name: Name of the Excel sheet
            **options: Additional options
            
        Returns:
            Excel content as bytes
        """
        try:
            import pandas as pd
            from io import BytesIO
            
            # Ensure data is a list of dictionaries
            if isinstance(data, dict):
                data = [data]
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Create Excel file in memory
            output = BytesIO()
            
            # Write to Excel
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets[sheet_name]
                for i, col in enumerate(df.columns):
                    max_width = max(
                        df[col].astype(str).map(len).max(),
                        len(str(col))
                    )
                    worksheet.set_column(i, i, max_width + 2)
            
            # Get the Excel content
            output.seek(0)
            return output.getvalue()
        
        except ImportError:
            logger.error("Pandas and xlsxwriter are required for Excel export")
            raise ImportError("Excel export requires pandas and xlsxwriter packages")
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = "",
                     sep: str = "_") -> Dict[str, Any]:
        """
        Flatten a nested dictionary for CSV export.
        
        Args:
            d: Dictionary to flatten
            parent_key: Parent key for nested items
            sep: Separator for nested keys
            
        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep).items())
            elif isinstance(v, list):
                # Convert list to string representation
                items.append((new_key, json.dumps(v)))
            else:
                items.append((new_key, v))
        
        return dict(items)
    
    def _dict_to_xml(self, d: Dict[str, Any], parent_element: ET.Element) -> None:
        """
        Convert a dictionary to XML elements.
        
        Args:
            d: Dictionary to convert
            parent_element: Parent XML element
        """
        for key, value in d.items():
            if value is None:
                # Skip None values
                continue
            
            if isinstance(value, dict):
                # Nested dictionary
                child = ET.SubElement(parent_element, str(key))
                self._dict_to_xml(value, child)
            elif isinstance(value, list):
                # List of items
                list_element = ET.SubElement(parent_element, str(key))
                
                for item in value:
                    if isinstance(item, dict):
                        item_element = ET.SubElement(list_element, "item")
                        self._dict_to_xml(item, item_element)
                    else:
                        # Simple value
                        item_element = ET.SubElement(list_element, "item")
                        item_element.text = str(item)
            else:
                # Simple value
                child = ET.SubElement(parent_element, str(key))
                child.text = str(value)
    
    def _json_serializer(self, obj: Any) -> Any:
        """
        JSON serializer for objects not serializable by default json code.
        
        Args:
            obj: Object to serialize
            
        Returns:
            Serialized object
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)
    
    def _ensure_extension(self, filename: str, format: str) -> str:
        """
        Ensure the filename has the correct extension.
        
        Args:
            filename: Original filename
            format: Export format
            
        Returns:
            Filename with correct extension
        """
        format = format.lower()
        _, ext = os.path.splitext(filename)
        
        # Map format to extension
        format_extensions = {
            "csv": ".csv",
            "json": ".json",
            "xml": ".xml",
            "excel": ".xlsx"
        }
        
        expected_ext = format_extensions.get(format)
        
        if not ext or ext.lower() != expected_ext:
            return f"{filename}{expected_ext}"
        
        return filename
    
    def bulk_export(self, data: Union[List[Dict[str, Any]], Dict[str, Any]],
                   formats: List[str], base_filename: str,
                   create_zip: bool = False, **options) -> Union[List[str], str]:
        """
        Export data to multiple formats at once.
        
        Args:
            data: Data to export
            formats: List of export formats
            base_filename: Base filename (without extension)
            create_zip: Whether to create a ZIP archive of all exports
            **options: Format-specific options
            
        Returns:
            List of output filenames, or the ZIP filename if create_zip is True
        """
        output_files = []
        
        for format in formats:
            if format not in self.FORMATS:
                logger.warning(f"Skipping unsupported format: {format}")
                continue
            
            # Export to each format
            filename = f"{base_filename}.{format}"
            output_file = self.export(data, format, filename, **options)
            output_files.append(output_file)
        
        # Create ZIP archive if requested
        if create_zip and output_files:
            zip_filename = f"{base_filename}.zip"
            
            with zipfile.ZipFile(zip_filename, "w") as zipf:
                for file in output_files:
                    zipf.write(file, os.path.basename(file))
            
            logger.info(f"Created ZIP archive: {zip_filename}")
            return zip_filename
        
        return output_files


# Create a singleton instance
_exporter = None

def get_exporter() -> DataExporter:
    """
    Get the global data exporter instance.
    
    Returns:
        DataExporter instance
    """
    global _exporter
    if _exporter is None:
        _exporter = DataExporter()
    return _exporter

def export_data(data: Union[List[Dict[str, Any]], Dict[str, Any]],
               format: str, filename: Optional[str] = None,
               **options) -> Union[str, bytes]:
    """
    Export data to the specified format using the global exporter.
    
    Args:
        data: Data to export
        format: Export format
        filename: Output filename
        **options: Format-specific options
        
    Returns:
        File content or output filename
    """
    return get_exporter().export(data, format, filename, **options)

def bulk_export(data: Union[List[Dict[str, Any]], Dict[str, Any]],
               formats: List[str], base_filename: str,
               create_zip: bool = False, **options) -> Union[List[str], str]:
    """
    Export data to multiple formats at once using the global exporter.
    
    Args:
        data: Data to export
        formats: List of export formats
        base_filename: Base filename (without extension)
        create_zip: Whether to create a ZIP archive
        **options: Format-specific options
        
    Returns:
        List of output filenames, or the ZIP filename
    """
    return get_exporter().bulk_export(data, formats, base_filename, create_zip, **options)