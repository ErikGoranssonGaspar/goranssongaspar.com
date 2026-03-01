"""Matplotlib styling module to match goranssongaspar.com website CSS."""

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Website colors from base.css
COLORS = {
    'bg': '#274c43',        # rgb(39, 76, 67) - blackboard green
    'text': '#E0F0E9',      # off-white/mint
    'primary': '#e6bb12',   # golden yellow
    'grid': '#E0F0E9',      # off-white for grid lines
    'secondary': '#ff7f50', # coral/salmon - complementary warm color
    'tertiary': '#5fb3b3',  # teal - cool accent color
}

# Font sizes in points (consistent across all figures)
FONT_SIZES = {
    'title': 16,
    'label': 14,
    'tick': 12,
    'legend': 11,
}

# Default figure size
DEFAULT_FIGSIZE = (10, 5)
DEFAULT_DPI = 100


def setup_matplotlib_style():
    """Configure matplotlib rcParams for website styling."""
    plt.rcParams.update({
        # Font settings
        'font.family': 'serif',
        'font.serif': ['CMU Serif', 'DejaVu Serif', 'serif'],
        'axes.titlesize': FONT_SIZES['title'],
        'axes.labelsize': FONT_SIZES['label'],
        'xtick.labelsize': FONT_SIZES['tick'],
        'ytick.labelsize': FONT_SIZES['tick'],
        'legend.fontsize': FONT_SIZES['legend'],
        
        # Fix minus sign rendering
        'axes.unicode_minus': False,
        
        # Colors
        'text.color': COLORS['text'],
        'axes.labelcolor': COLORS['text'],
        'xtick.color': COLORS['text'],
        'ytick.color': COLORS['text'],
        'axes.edgecolor': COLORS['text'],
        
        # Grid
        'axes.grid': True,
        'grid.color': COLORS['grid'],
        'grid.alpha': 0.2,
        'grid.linestyle': '-',
        'grid.linewidth': 0.8,
        
        # Figure
        'figure.facecolor': COLORS['bg'],
        'axes.facecolor': COLORS['bg'],
        'savefig.facecolor': COLORS['bg'],
        'savefig.edgecolor': 'none',
        
        # Legend
        'legend.facecolor': COLORS['bg'],
        'legend.edgecolor': COLORS['text'],
        'legend.labelcolor': COLORS['text'],
        'legend.framealpha': 0.95,
    })


def create_styled_figure(figsize=DEFAULT_FIGSIZE, nrows=1, ncols=1, dpi=DEFAULT_DPI):
    """
    Create a figure and axes with website styling applied.
    
    Parameters
    ----------
    figsize : tuple
        Figure size in inches (width, height)
    nrows, ncols : int
        Number of subplot rows and columns
    dpi : int
        Figure DPI
        
    Returns
    -------
    fig : matplotlib.figure.Figure
    axes : matplotlib.axes.Axes or array of Axes
    """
    setup_matplotlib_style()
    
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, dpi=dpi)
    
    # Ensure axes is always iterable (even for single subplot)
    if nrows == 1 and ncols == 1:
        axes = [axes]
    elif nrows == 1 or ncols == 1:
        axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]
    else:
        axes = axes.flatten()
    
    # Apply styling to each axis
    for ax in axes:
        # Style spines - keep all visible for full border
        for spine in ax.spines.values():
            spine.set_color(COLORS['text'])
            spine.set_linewidth(1.0)
        
        # Ensure tick colors
        ax.tick_params(axis='both', colors=COLORS['text'])
        
        # Grid is already enabled via rcParams, but ensure it's visible
        ax.grid(True, alpha=0.2, color=COLORS['grid'], linestyle='-', linewidth=0.8)
    
    return fig, axes[0] if len(axes) == 1 else axes


def style_legend(ax, **kwargs):
    """
    Apply website styling to a legend.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes containing the legend
    **kwargs : additional arguments passed to ax.legend()
    """
    legend = ax.legend(
        facecolor=COLORS['bg'],
        edgecolor=COLORS['text'],
        framealpha=0.95,
        **kwargs
    )
    
    if legend:
        for text in legend.get_texts():
            text.set_color(COLORS['text'])
        legend.get_frame().set_facecolor(COLORS['bg'])
        legend.get_frame().set_edgecolor(COLORS['text'])
    
    return legend


def format_datetime_axis(ax, dates=None, format_str='%b'):
    """
    Format x-axis with 3-letter month names.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to format
    dates : array-like, optional
        Date values (if not already set as x-data)
    format_str : str
        Date format string (default '%b' for 3-letter month)
    """
    ax.xaxis.set_major_formatter(DateFormatter(format_str))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center')
    
    # Ensure tick labels are visible and styled
    for label in ax.get_xticklabels():
        label.set_color(COLORS['text'])
        label.set_fontsize(FONT_SIZES['tick'])


def save_styled_figure(fig, filepath, bbox_inches='tight', pad_inches=0.1, **kwargs):
    """
    Save a figure with website styling.
    
    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to save
    filepath : str or Path
        Output file path
    bbox_inches : str
        Bounding box setting
    pad_inches : float
        Padding around the figure
    **kwargs : additional arguments passed to fig.savefig()
    """
    fig.savefig(
        filepath,
        bbox_inches=bbox_inches,
        pad_inches=pad_inches,
        facecolor=COLORS['bg'],
        edgecolor='none',
        **kwargs
    )
