"""
Data Visualization Utilities for BloxAPI

This module provides functionality for generating visualizations and charts
from API data. It supports various chart types and export formats.
"""

import io
import base64
import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)

class Visualization:
    """
    Base class for all visualizations
    """
    
    def __init__(self, title: str = "", width: int = 10, height: int = 6, 
                dpi: int = 100, theme: str = "default"):
        """
        Initialize visualization
        
        Args:
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Resolution in dots per inch
            theme: Visual theme (default, dark, light, etc.)
        """
        self.title = title
        self.width = width
        self.height = height
        self.dpi = dpi
        self.theme = theme
        
        # Apply theme
        self.apply_theme(theme)
        
        # Create figure and axes
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        
        # Set title if provided
        if title:
            self.fig.suptitle(title)
    
    def apply_theme(self, theme: str) -> None:
        """
        Apply a visual theme to the visualization
        
        Args:
            theme: Theme name
        """
        if theme == "dark":
            plt.style.use('dark_background')
        elif theme == "light":
            plt.style.use('seaborn-v0_8-whitegrid')
        elif theme == "minimal":
            plt.style.use('seaborn-v0_8-white')
        elif theme == "colorful":
            plt.style.use('seaborn-v0_8-colorblind')
        else:
            plt.style.use('default')
    
    def to_image(self, format: str = "png") -> bytes:
        """
        Convert the visualization to an image
        
        Args:
            format: Image format (png, jpg, svg, pdf)
            
        Returns:
            Image data as bytes
        """
        # Adjust layout
        plt.tight_layout()
        
        # Save to bytes buffer
        buf = io.BytesIO()
        self.fig.savefig(buf, format=format)
        buf.seek(0)
        
        # Close the figure to free memory
        plt.close(self.fig)
        
        return buf.getvalue()
    
    def to_base64(self, format: str = "png") -> str:
        """
        Convert the visualization to a base64-encoded string
        
        Args:
            format: Image format (png, jpg, svg, pdf)
            
        Returns:
            Base64-encoded image data
        """
        image_data = self.to_image(format)
        encoded = base64.b64encode(image_data).decode("utf-8")
        return f"data:image/{format};base64,{encoded}"
    
    def save(self, filename: str) -> str:
        """
        Save the visualization to a file
        
        Args:
            filename: Output filename
            
        Returns:
            Output filename
        """
        # Adjust layout
        plt.tight_layout()
        
        # Save to file
        self.fig.savefig(filename)
        
        # Close the figure to free memory
        plt.close(self.fig)
        
        logger.info(f"Saved visualization to {filename}")
        return filename


class LineChart(Visualization):
    """
    Line chart visualization
    """
    
    def __init__(self, title: str = "", width: int = 10, height: int = 6, 
                dpi: int = 100, theme: str = "default"):
        """
        Initialize line chart
        
        Args:
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Resolution in dots per inch
            theme: Visual theme
        """
        super().__init__(title, width, height, dpi, theme)
    
    def plot(self, data: Dict[str, List], x_label: str = "", y_label: str = "",
            legend: bool = True, grid: bool = True, marker: Optional[str] = None,
            line_style: str = "-", colors: Optional[List[str]] = None) -> "LineChart":
        """
        Plot data on the line chart
        
        Args:
            data: Dictionary mapping series names to lists of y values,
                 or x values and y values as {'x': [...], 'series1': [...], 'series2': [...]}
            x_label: Label for x-axis
            y_label: Label for y-axis
            legend: Whether to show legend
            grid: Whether to show grid
            marker: Marker style (e.g. 'o', '.', None for no markers)
            line_style: Line style (e.g. '-', '--', ':', '-.')
            colors: List of colors for each series
            
        Returns:
            Self for method chaining
        """
        # Check if x values are provided
        if 'x' in data:
            x_values = data.pop('x')
            
            # Check if x values are dates or datetime strings
            if isinstance(x_values[0], str):
                try:
                    x_values = [datetime.fromisoformat(x) if 'T' in x 
                              else datetime.strptime(x, "%Y-%m-%d") 
                              for x in x_values]
                    
                    # Format x-axis for dates
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                    self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                except ValueError:
                    # Not dates, keep as strings
                    pass
        else:
            # Use indices as x values
            first_series = list(data.values())[0]
            x_values = list(range(len(first_series)))
        
        # Plot each series
        for i, (name, y_values) in enumerate(data.items()):
            color = colors[i] if colors and i < len(colors) else None
            self.ax.plot(x_values, y_values, label=name, marker=marker, 
                       linestyle=line_style, color=color)
        
        # Set labels
        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)
        
        # Show legend if requested
        if legend and len(data) > 1:
            self.ax.legend()
        
        # Show grid if requested
        self.ax.grid(grid)
        
        # Format the figure
        self.fig.tight_layout()
        
        return self


class BarChart(Visualization):
    """
    Bar chart visualization
    """
    
    def __init__(self, title: str = "", width: int = 10, height: int = 6, 
                dpi: int = 100, theme: str = "default", horizontal: bool = False):
        """
        Initialize bar chart
        
        Args:
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Resolution in dots per inch
            theme: Visual theme
            horizontal: Whether to create a horizontal bar chart
        """
        super().__init__(title, width, height, dpi, theme)
        self.horizontal = horizontal
    
    def plot(self, data: Dict[str, Union[List, float, int]], x_label: str = "", 
            y_label: str = "", legend: bool = True, grid: bool = True,
            colors: Optional[List[str]] = None, stacked: bool = False) -> "BarChart":
        """
        Plot data on the bar chart
        
        Args:
            data: Dictionary mapping categories to values,
                 or categories to lists of values for grouped bars
            x_label: Label for x-axis
            y_label: Label for y-axis
            legend: Whether to show legend
            grid: Whether to show grid
            colors: List of colors for bars
            stacked: Whether to create a stacked bar chart
            
        Returns:
            Self for method chaining
        """
        # Determine if we have grouped/stacked bars or simple bars
        is_grouped = any(isinstance(v, list) for v in data.values())
        
        if is_grouped:
            # Grouped or stacked bars
            categories = list(data.keys())
            
            # All series should have the same length
            series_length = len(list(data.values())[0])
            
            # Extract series names from first category's data if it's a dict
            if isinstance(list(data.values())[0], dict):
                series_names = list(list(data.values())[0].keys())
                # Convert to lists
                data = {k: [v.get(s, 0) for s in series_names] for k, v in data.items()}
            else:
                series_names = [f"Series {i+1}" for i in range(series_length)]
            
            # Set up positions
            pos = np.arange(len(categories))
            width = 0.8 / series_length if not stacked else 0.8
            
            # Plot each series
            for i in range(series_length):
                values = [d[i] if i < len(d) else 0 for d in data.values()]
                bottom = None
                
                if stacked and i > 0:
                    # Calculate bottom for stacked bars
                    bottom = np.zeros(len(categories))
                    for j in range(i):
                        for k, category in enumerate(categories):
                            if j < len(data[category]):
                                bottom[k] += data[category][j]
                
                color = colors[i] if colors and i < len(colors) else None
                
                if self.horizontal:
                    self.ax.barh(pos, values, height=width, 
                               left=bottom, label=series_names[i], color=color)
                else:
                    self.ax.bar(pos if not stacked else pos, values, width=width, 
                              bottom=bottom, label=series_names[i], color=color)
            
            # Set category labels
            if self.horizontal:
                self.ax.set_yticks(pos)
                self.ax.set_yticklabels(categories)
            else:
                self.ax.set_xticks(pos)
                self.ax.set_xticklabels(categories)
        else:
            # Simple bars
            categories = list(data.keys())
            values = list(data.values())
            
            if self.horizontal:
                self.ax.barh(categories, values, color=colors)
            else:
                self.ax.bar(categories, values, color=colors)
        
        # Set labels
        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)
        
        # Show legend if requested and we have grouped bars
        if legend and is_grouped:
            self.ax.legend()
        
        # Show grid if requested
        self.ax.grid(grid, axis='both' if grid else 'y')
        
        # Format the figure
        self.fig.tight_layout()
        
        return self


class PieChart(Visualization):
    """
    Pie chart visualization
    """
    
    def __init__(self, title: str = "", width: int = 8, height: int = 8, 
                dpi: int = 100, theme: str = "default"):
        """
        Initialize pie chart
        
        Args:
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Resolution in dots per inch
            theme: Visual theme
        """
        super().__init__(title, width, height, dpi, theme)
    
    def plot(self, data: Dict[str, Union[float, int]], 
            colors: Optional[List[str]] = None, explode: Optional[List[float]] = None,
            shadow: bool = False, start_angle: int = 0, 
            autopct: str = '%1.1f%%') -> "PieChart":
        """
        Plot data on the pie chart
        
        Args:
            data: Dictionary mapping categories to values
            colors: List of colors for slices
            explode: List of explosion values for each slice
            shadow: Whether to add a shadow
            start_angle: Starting angle for the first slice
            autopct: Format for percentage labels
            
        Returns:
            Self for method chaining
        """
        # Extract categories and values
        categories = list(data.keys())
        values = list(data.values())
        
        # Create pie chart
        self.ax.pie(
            values,
            labels=categories,
            colors=colors,
            explode=explode,
            shadow=shadow,
            startangle=start_angle,
            autopct=autopct
        )
        
        # Equal aspect ratio ensures circular pie
        self.ax.axis('equal')
        
        # Format the figure
        self.fig.tight_layout()
        
        return self


class ScatterPlot(Visualization):
    """
    Scatter plot visualization
    """
    
    def __init__(self, title: str = "", width: int = 10, height: int = 6, 
                dpi: int = 100, theme: str = "default"):
        """
        Initialize scatter plot
        
        Args:
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Resolution in dots per inch
            theme: Visual theme
        """
        super().__init__(title, width, height, dpi, theme)
    
    def plot(self, data: Dict[str, Tuple[List, List]], x_label: str = "", 
            y_label: str = "", legend: bool = True, grid: bool = True,
            colors: Optional[List[str]] = None, sizes: Optional[List[float]] = None,
            alpha: float = 0.7, marker: str = 'o') -> "ScatterPlot":
        """
        Plot data on the scatter plot
        
        Args:
            data: Dictionary mapping series names to tuples of (x_values, y_values)
            x_label: Label for x-axis
            y_label: Label for y-axis
            legend: Whether to show legend
            grid: Whether to show grid
            colors: List of colors for series
            sizes: List of point sizes
            alpha: Transparency level
            marker: Marker style
            
        Returns:
            Self for method chaining
        """
        # Plot each series
        for i, (name, (x_values, y_values)) in enumerate(data.items()):
            color = colors[i] if colors and i < len(colors) else None
            size = sizes[i] if sizes and i < len(sizes) else None
            
            self.ax.scatter(
                x_values, 
                y_values, 
                label=name, 
                color=color, 
                s=size, 
                alpha=alpha, 
                marker=marker
            )
        
        # Set labels
        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)
        
        # Show legend if requested
        if legend and len(data) > 1:
            self.ax.legend()
        
        # Show grid if requested
        self.ax.grid(grid)
        
        # Format the figure
        self.fig.tight_layout()
        
        return self


class Heatmap(Visualization):
    """
    Heatmap visualization
    """
    
    def __init__(self, title: str = "", width: int = 10, height: int = 8, 
                dpi: int = 100, theme: str = "default"):
        """
        Initialize heatmap
        
        Args:
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Resolution in dots per inch
            theme: Visual theme
        """
        super().__init__(title, width, height, dpi, theme)
    
    def plot(self, data: List[List[float]], x_labels: Optional[List[str]] = None, 
            y_labels: Optional[List[str]] = None, cmap: str = 'viridis',
            show_values: bool = False, colorbar: bool = True) -> "Heatmap":
        """
        Plot data on the heatmap
        
        Args:
            data: 2D list/array of values
            x_labels: Labels for x-axis
            y_labels: Labels for y-axis
            cmap: Colormap name
            show_values: Whether to show values on cells
            colorbar: Whether to show colorbar
            
        Returns:
            Self for method chaining
        """
        # Create heatmap
        im = self.ax.imshow(data, cmap=cmap)
        
        # Show colorbar if requested
        if colorbar:
            self.fig.colorbar(im, ax=self.ax)
        
        # Set labels
        if x_labels:
            self.ax.set_xticks(np.arange(len(x_labels)))
            self.ax.set_xticklabels(x_labels)
            plt.setp(self.ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
            
        if y_labels:
            self.ax.set_yticks(np.arange(len(y_labels)))
            self.ax.set_yticklabels(y_labels)
        
        # Show values on cells if requested
        if show_values:
            for i in range(len(data)):
                for j in range(len(data[i])):
                    text_color = 'white' if data[i][j] > np.mean(data) else 'black'
                    self.ax.text(j, i, format(data[i][j], '.2f'),
                               ha="center", va="center", color=text_color)
        
        # Format the figure
        self.fig.tight_layout()
        
        return self


class HistogramChart(Visualization):
    """
    Histogram visualization
    """
    
    def __init__(self, title: str = "", width: int = 10, height: int = 6, 
                dpi: int = 100, theme: str = "default"):
        """
        Initialize histogram
        
        Args:
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Resolution in dots per inch
            theme: Visual theme
        """
        super().__init__(title, width, height, dpi, theme)
    
    def plot(self, data: Dict[str, List[float]], x_label: str = "", 
            y_label: str = "Frequency", legend: bool = True, grid: bool = True,
            bins: Union[int, List[float]] = 10, density: bool = False,
            cumulative: bool = False, colors: Optional[List[str]] = None,
            alpha: float = 0.7) -> "HistogramChart":
        """
        Plot data on the histogram
        
        Args:
            data: Dictionary mapping series names to lists of values
            x_label: Label for x-axis
            y_label: Label for y-axis
            legend: Whether to show legend
            grid: Whether to show grid
            bins: Number of bins or bin edges
            density: Whether to normalize the histogram
            cumulative: Whether to plot a cumulative histogram
            colors: List of colors for series
            alpha: Transparency level
            
        Returns:
            Self for method chaining
        """
        # Plot each series
        for i, (name, values) in enumerate(data.items()):
            color = colors[i] if colors and i < len(colors) else None
            
            self.ax.hist(
                values,
                bins=bins,
                label=name,
                density=density,
                cumulative=cumulative,
                alpha=alpha,
                color=color,
                edgecolor='black'
            )
        
        # Set labels
        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)
        
        # Show legend if requested
        if legend and len(data) > 1:
            self.ax.legend()
        
        # Show grid if requested
        self.ax.grid(grid)
        
        # Format the figure
        self.fig.tight_layout()
        
        return self


class BoxPlot(Visualization):
    """
    Box plot visualization
    """
    
    def __init__(self, title: str = "", width: int = 10, height: int = 6, 
                dpi: int = 100, theme: str = "default", horizontal: bool = False):
        """
        Initialize box plot
        
        Args:
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Resolution in dots per inch
            theme: Visual theme
            horizontal: Whether to create a horizontal box plot
        """
        super().__init__(title, width, height, dpi, theme)
        self.horizontal = horizontal
    
    def plot(self, data: Dict[str, List[float]], x_label: str = "", 
            y_label: str = "", grid: bool = True, notch: bool = False,
            colors: Optional[List[str]] = None, flierprops: Optional[Dict] = None,
            boxprops: Optional[Dict] = None, whiskerprops: Optional[Dict] = None,
            capprops: Optional[Dict] = None, medianprops: Optional[Dict] = None) -> "BoxPlot":
        """
        Plot data on the box plot
        
        Args:
            data: Dictionary mapping categories to lists of values
            x_label: Label for x-axis
            y_label: Label for y-axis
            grid: Whether to show grid
            notch: Whether to create notched box plots
            colors: List of colors for boxes
            flierprops: Properties for outlier markers
            boxprops: Properties for boxes
            whiskerprops: Properties for whiskers
            capprops: Properties for caps
            medianprops: Properties for median lines
            
        Returns:
            Self for method chaining
        """
        # Extract categories and values
        categories = list(data.keys())
        values = list(data.values())
        
        # Set default properties if not provided
        if flierprops is None:
            flierprops = {'marker': 'o', 'markersize': 5}
        if boxprops is None and colors:
            boxprops = {'facecolor': 'none'}
        
        # Create box plot
        if self.horizontal:
            boxplot = self.ax.boxplot(
                values,
                labels=categories,
                notch=notch,
                patch_artist=True,
                flierprops=flierprops,
                boxprops=boxprops,
                whiskerprops=whiskerprops,
                capprops=capprops,
                medianprops=medianprops,
                vert=False
            )
        else:
            boxplot = self.ax.boxplot(
                values,
                labels=categories,
                notch=notch,
                patch_artist=True,
                flierprops=flierprops,
                boxprops=boxprops,
                whiskerprops=whiskerprops,
                capprops=capprops,
                medianprops=medianprops
            )
        
        # Color boxes if colors are provided
        if colors:
            for i, box in enumerate(boxplot['boxes']):
                color = colors[i % len(colors)]
                box.set_facecolor(color)
        
        # Set labels
        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)
        
        # Show grid if requested
        self.ax.grid(grid, axis='both' if grid else 'y')
        
        # Format the figure
        self.fig.tight_layout()
        
        return self


class RadarChart(Visualization):
    """
    Radar chart visualization
    """
    
    def __init__(self, title: str = "", width: int = 8, height: int = 8, 
                dpi: int = 100, theme: str = "default"):
        """
        Initialize radar chart
        
        Args:
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Resolution in dots per inch
            theme: Visual theme
        """
        super().__init__(title, width, height, dpi, theme)
        
        # Create polar projection
        self.fig, self.ax = plt.subplots(figsize=(width, height), 
                                      dpi=dpi, subplot_kw=dict(polar=True))
        
        # Set title if provided
        if title:
            self.fig.suptitle(title)
    
    def plot(self, data: Dict[str, List[float]], categories: List[str],
            legend: bool = True, grid: bool = True, colors: Optional[List[str]] = None,
            fill: bool = True, alpha: float = 0.25) -> "RadarChart":
        """
        Plot data on the radar chart
        
        Args:
            data: Dictionary mapping series names to lists of values
            categories: List of category names
            legend: Whether to show legend
            grid: Whether to show grid
            colors: List of colors for series
            fill: Whether to fill the radar chart
            alpha: Transparency level for fill
            
        Returns:
            Self for method chaining
        """
        # Compute angle for each category
        n = len(categories)
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
        
        # Close the polygon
        angles += angles[:1]
        
        # Set category labels
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(categories)
        
        # Plot each series
        for i, (name, values) in enumerate(data.items()):
            # Close the polygon
            values = values + [values[0]]
            
            color = colors[i] if colors and i < len(colors) else None
            
            # Plot series
            self.ax.plot(angles, values, label=name, color=color)
            
            # Fill the area if requested
            if fill:
                self.ax.fill(angles, values, alpha=alpha, color=color)
        
        # Show legend if requested
        if legend and len(data) > 1:
            self.ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        # Show grid if requested
        self.ax.grid(grid)
        
        # Format the figure
        self.fig.tight_layout()
        
        return self


class BubbleChart(Visualization):
    """
    Bubble chart visualization
    """
    
    def __init__(self, title: str = "", width: int = 10, height: int = 6, 
                dpi: int = 100, theme: str = "default"):
        """
        Initialize bubble chart
        
        Args:
            title: Chart title
            width: Figure width in inches
            height: Figure height in inches
            dpi: Resolution in dots per inch
            theme: Visual theme
        """
        super().__init__(title, width, height, dpi, theme)
    
    def plot(self, data: Dict[str, Tuple[List, List, List]], x_label: str = "", 
            y_label: str = "", legend: bool = True, grid: bool = True,
            colors: Optional[List[str]] = None, alpha: float = 0.7,
            size_scale: float = 1000, min_size: float = 10) -> "BubbleChart":
        """
        Plot data on the bubble chart
        
        Args:
            data: Dictionary mapping series names to tuples of (x_values, y_values, sizes)
            x_label: Label for x-axis
            y_label: Label for y-axis
            legend: Whether to show legend
            grid: Whether to show grid
            colors: List of colors for series
            alpha: Transparency level
            size_scale: Scaling factor for bubble sizes
            min_size: Minimum bubble size
            
        Returns:
            Self for method chaining
        """
        # Plot each series
        for i, (name, (x_values, y_values, sizes)) in enumerate(data.items()):
            color = colors[i] if colors and i < len(colors) else None
            
            # Scale sizes
            scaled_sizes = [max(s * size_scale, min_size) for s in sizes]
            
            self.ax.scatter(
                x_values, 
                y_values, 
                s=scaled_sizes, 
                label=name, 
                color=color, 
                alpha=alpha
            )
        
        # Set labels
        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)
        
        # Show legend if requested
        if legend and len(data) > 1:
            self.ax.legend()
        
        # Show grid if requested
        self.ax.grid(grid)
        
        # Format the figure
        self.fig.tight_layout()
        
        return self


class VisualizationFactory:
    """
    Factory for creating visualizations
    """
    
    @staticmethod
    def create(chart_type: str, **kwargs) -> Visualization:
        """
        Create a visualization of the specified type
        
        Args:
            chart_type: Type of chart to create
            **kwargs: Additional arguments for the visualization
            
        Returns:
            Visualization instance
        """
        chart_type = chart_type.lower()
        
        if chart_type == "line":
            return LineChart(**kwargs)
        elif chart_type == "bar":
            return BarChart(**kwargs)
        elif chart_type == "horizontal_bar":
            return BarChart(horizontal=True, **kwargs)
        elif chart_type == "pie":
            return PieChart(**kwargs)
        elif chart_type == "scatter":
            return ScatterPlot(**kwargs)
        elif chart_type == "heatmap":
            return Heatmap(**kwargs)
        elif chart_type == "histogram":
            return HistogramChart(**kwargs)
        elif chart_type == "box":
            return BoxPlot(**kwargs)
        elif chart_type == "horizontal_box":
            return BoxPlot(horizontal=True, **kwargs)
        elif chart_type == "radar":
            return RadarChart(**kwargs)
        elif chart_type == "bubble":
            return BubbleChart(**kwargs)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")


def create_visualization(chart_type: str, data: Dict[str, Any], **kwargs) -> Visualization:
    """
    Create and plot a visualization
    
    Args:
        chart_type: Type of chart to create
        data: Data to plot
        **kwargs: Additional arguments for the visualization
        
    Returns:
        Plotted visualization
    """
    # Extract visualization-specific kwargs
    viz_kwargs = {k: v for k, v in kwargs.items() 
                if k in ["title", "width", "height", "dpi", "theme"]}
    
    # Extract plot-specific kwargs
    plot_kwargs = {k: v for k, v in kwargs.items() if k not in viz_kwargs}
    
    # Create the visualization
    viz = VisualizationFactory.create(chart_type, **viz_kwargs)
    
    # Plot the data
    return viz.plot(data, **plot_kwargs)


def to_image(chart_type: str, data: Dict[str, Any], format: str = "png", **kwargs) -> bytes:
    """
    Create a visualization and convert it to an image
    
    Args:
        chart_type: Type of chart to create
        data: Data to plot
        format: Image format
        **kwargs: Additional arguments for the visualization
        
    Returns:
        Image data as bytes
    """
    viz = create_visualization(chart_type, data, **kwargs)
    return viz.to_image(format)


def to_base64(chart_type: str, data: Dict[str, Any], format: str = "png", **kwargs) -> str:
    """
    Create a visualization and convert it to a base64-encoded string
    
    Args:
        chart_type: Type of chart to create
        data: Data to plot
        format: Image format
        **kwargs: Additional arguments for the visualization
        
    Returns:
        Base64-encoded image data
    """
    viz = create_visualization(chart_type, data, **kwargs)
    return viz.to_base64(format)


def save_chart(chart_type: str, data: Dict[str, Any], filename: str, **kwargs) -> str:
    """
    Create a visualization and save it to a file
    
    Args:
        chart_type: Type of chart to create
        data: Data to plot
        filename: Output filename
        **kwargs: Additional arguments for the visualization
        
    Returns:
        Output filename
    """
    viz = create_visualization(chart_type, data, **kwargs)
    return viz.save(filename)