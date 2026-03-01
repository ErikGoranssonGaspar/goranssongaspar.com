# Plot Styling Guide for goranssongaspar.com

This document provides guidelines for creating plots that match the website's visual style.

## Quick Start

```python
from plot_style import (
    COLORS, FONT_SIZES,
    create_styled_figure, style_legend, 
    format_datetime_axis, save_styled_figure
)

# Create a basic figure
fig, ax = create_styled_figure(figsize=(10, 5))
ax.plot(x, y, color=COLORS['primary'], linewidth=2)
ax.set_title('Plot Title', fontsize=FONT_SIZES['title'])
ax.set_ylabel('Y Label', fontsize=FONT_SIZES['label'])
format_datetime_axis(ax)  # For date x-axes
plt.tight_layout()
save_styled_figure(fig, 'output.svg')
```

## Website Style Guide

### Colors (from base.css)

All plots use these colors from `Code/goranssongaspar.com/static/styles/base.css`:

| Color | Hex Code | CSS Variable | Usage |
|-------|----------|--------------|-------|
| Background | `#274c43` | `--blackboard-green` | Figure/axes background |
| Text | `#E0F0E9` | `--text-color` | Labels, ticks, titles, spines |
| Primary (Golden) | `#e6bb12` | `--pico-primary` | Main data lines, histograms |
| Secondary (Coral) | `#ff7f50` | - | Secondary lines, confidence intervals |
| Tertiary (Teal) | `#5fb3b3` | - | Third data series |
| Grid | `#E0F0E9` | - | Grid lines (alpha=0.2) |

**Python access:**
```python
from plot_style import COLORS
bg_color = COLORS['bg']           # #274c43
text_color = COLORS['text']       # #E0F0E9
primary_color = COLORS['primary'] # #e6bb12
secondary_color = COLORS['secondary'] # #ff7f50
tertiary_color = COLORS['tertiary']   # #5fb3b3
```

### Typography

- **Font Family**: CMU Serif (Computer Modern Unicode Serif)
- **Font Sizes**:
  - Title: 16pt
  - Axis labels: 14pt  
  - Tick labels: 12pt
  - Legend: 11pt

**Python access:**
```python
from plot_style import FONT_SIZES
title_size = FONT_SIZES['title']    # 16
label_size = FONT_SIZES['label']    # 14
tick_size = FONT_SIZES['tick']      # 12
legend_size = FONT_SIZES['legend']  # 11
```

### Figure Specifications

#### Standard Sizes
- **Single plot**: `(10, 5)` inches (width, height)
- **Square plots**: `(5, 5)` inches (for side-by-side comparison)
- **Multi-panel (3 rows)**: `(10, 9)` inches
- **Multi-panel (2×2)**: `(10, 8)` inches

#### Key Style Elements
1. **Full border**: All 4 spines visible (not just bottom/left)
2. **Grid lines**: Solid, alpha=0.2, off-white color
3. **No transparency** on main plot elements (except grid)
4. **Dashed reference lines**: White (`COLORS['text']`), fully opaque (no alpha)
5. **Date formatting**: 3-letter month names (Jan, Feb, Mar, etc.)

## The Styling Module

### Location
`Code/goranssongaspar.com/static/doc/ou_cox_timing_PM/plot_style.py`

### Functions

#### `create_styled_figure(figsize=(10, 5), nrows=1, ncols=1, dpi=100)`
Creates a figure with website styling pre-applied.

**Parameters:**
- `figsize`: Tuple of (width, height) in inches
- `nrows`, `ncols`: Number of subplot rows/columns
- `dpi`: Resolution (default 100)

**Returns:** `(fig, axes)` - matplotlib figure and axes

**Example:**
```python
# Single plot
fig, ax = create_styled_figure(figsize=(10, 5))

# 3 subplots vertically
fig, (ax1, ax2, ax3) = create_styled_figure(nrows=3, ncols=1, figsize=(10, 9))

# 2x2 grid
fig, axes = create_styled_figure(nrows=2, ncols=2, figsize=(10, 8))
axes = axes.flatten()  # Access as axes[0], axes[1], etc.
```

#### `style_legend(ax, **kwargs)`
Applies website styling to a legend.

**Parameters:**
- `ax`: Matplotlib axes object
- `**kwargs`: Additional arguments passed to `ax.legend()`

**Example:**
```python
style_legend(ax, loc='upper right')
style_legend(ax, loc='center left', bbox_to_anchor=(1.02, 0.5), frameon=False)
```

#### `format_datetime_axis(ax, format_str='%b')`
Formats x-axis with 3-letter month names.

**Parameters:**
- `ax`: Matplotlib axes object
- `format_str`: Date format (default '%b' for 3-letter months)

**Example:**
```python
format_datetime_axis(ax)  # Shows Jan, Feb, Mar, etc.
```

#### `save_styled_figure(fig, filepath, bbox_inches='tight', pad_inches=0.1)`
Saves figure with proper styling.

**Parameters:**
- `fig`: Matplotlib figure object
- `filepath`: Output path (e.g., 'figure.svg')
- `bbox_inches`: Bounding box setting (default 'tight')
- `pad_inches`: Padding around figure (default 0.1)

**Example:**
```python
save_styled_figure(fig, 'output.svg')
```

## Common Plot Patterns

### Single Time Series (like Figure 2)

```python
fig, ax = create_styled_figure(figsize=(10, 5))
ax.plot(dates, prices * 100, color=COLORS['primary'], linewidth=2)
ax.set_title('Yes-Price for "Market Name"', fontsize=FONT_SIZES['title'])
ax.set_ylabel('Price (US¢)', fontsize=FONT_SIZES['label'])
ax.set_ylim(-5, 105)  # For price data
format_datetime_axis(ax)
plt.tight_layout()
save_styled_figure(fig, 'output.svg')
```

### Multi-Panel with Shared X-Axis (like Figure 3)

```python
fig, (ax0, ax1, ax2) = create_styled_figure(nrows=3, ncols=1, figsize=(10, 9))

# Top subplot
ax0.plot(dates, prices, color=COLORS['primary'], linewidth=2)
ax0.set_title('Price', fontsize=FONT_SIZES['title'])
ax0.set_ylabel('Price', fontsize=FONT_SIZES['label'])
ax0.tick_params(axis='x', labelbottom=False)  # Hide x-labels

# Middle subplot
ax1.plot(dates, intensity, color=COLORS['primary'], linewidth=2)
ax1.set_title('Intensity', fontsize=FONT_SIZES['title'])
ax1.set_ylabel('Intensity', fontsize=FONT_SIZES['label'])
ax1.tick_params(axis='x', labelbottom=False)

# Bottom subplot
ax2.plot(dates, series1, color=COLORS['secondary'], label='Series 1')
ax2.plot(dates, series2, color=COLORS['primary'], label='Series 2')
ax2.set_title('Volatility', fontsize=FONT_SIZES['title'])
ax2.set_ylabel('Volatility', fontsize=FONT_SIZES['label'])
format_datetime_axis(ax2)  # Only on bottom
style_legend(ax2, loc='upper right')

plt.tight_layout()
save_styled_figure(fig, 'output.svg')
```

### Forecast with Confidence Intervals (like Figure 4)

```python
fig, ax = create_styled_figure(figsize=(10, 5))

# Vertical line at forecast start (white, dashed, opaque)
ax.axvline(start_date, color=COLORS['text'], linestyle='--', linewidth=1.5)

# Historical data
ax.plot(historical_dates, historical_prices, 
        color=COLORS['primary'], linewidth=2, label='Historical')

# Forecast mean
ax.plot(forecast_dates, forecast_mean, 
        color=COLORS['secondary'], linewidth=2, label='MC Mean')

# Confidence interval (coral fill with transparency)
ax.fill_between(forecast_dates, lower_bound, upper_bound,
                color=COLORS['secondary'], alpha=0.3)

ax.set_title('Title', fontsize=FONT_SIZES['title'])
style_legend(ax, loc='upper right')
plt.tight_layout()
save_styled_figure(fig, 'output.svg')
```

### Side-by-Side Comparison (like Figures 5a/b)

```python
# Figure 5a
fig, ax = create_styled_figure(figsize=(5, 5))  # Square
ax.plot(x, y, color=COLORS['primary'], linewidth=2.5)
ax.axhline(reference, color=COLORS['text'], linestyle='--', linewidth=2,
           label='Reference line')  # No alpha!
ax.set_xlabel('X Label', fontsize=FONT_SIZES['label'])
ax.set_ylabel('Y Label', fontsize=FONT_SIZES['label'])
ax.set_title('Plot Title', fontsize=FONT_SIZES['title'])
style_legend(ax, loc='lower right')
plt.tight_layout()
save_styled_figure(fig, 'figure_a.svg')

# Figure 5b - similar but with different data
# ... create separately
```

### Diagnostics Grid (like Figure 6)

```python
fig, axes = create_styled_figure(nrows=2, ncols=2, figsize=(10, 8))
axes = axes.flatten()

# Histogram - no transparency, no edge
axes[0].hist(data, bins=30, density=True, color=COLORS['primary'], edgecolor='none')
axes[0].set_title('Histogram', fontsize=FONT_SIZES['title'])

# QQ-plot with white dashed reference line
stats.probplot(data, dist="norm", plot=axes[1])
lines = axes[1].lines
lines[0].set_color(COLORS['primary'])  # Data points
lines[0].set_markerfacecolor(COLORS['primary'])
lines[1].set_color(COLORS['text'])      # Reference line
lines[1].set_linestyle('--')
lines[1].set_linewidth(1.5)
axes[1].set_title('QQ-Plot', fontsize=FONT_SIZES['title'])

# ACF plots with ylim(-0.3, 1.1)
plot_acf(data, lags=nlags, ax=axes[2], color=COLORS['primary'])
axes[2].set_ylim(-0.3, 1.1)
axes[2].set_title('ACF', fontsize=FONT_SIZES['title'])

# Style all ACF elements to primary color
for line in axes[2].lines:
    line.set_color(COLORS['primary'])
for collection in axes[2].collections:
    collection.set_facecolor(COLORS['primary'])
    collection.set_edgecolor(COLORS['primary'])

plt.tight_layout()
save_styled_figure(fig, 'diagnostics.svg')
```

### Calibration Plot (like Figure 7)

```python
fig, ax = create_styled_figure(figsize=(7, 7))
ax.plot(x, y, color=COLORS['primary'], linewidth=2.5, label='Empirical')
ax.plot(x, x, color=COLORS['text'], linestyle='--', linewidth=2,  # No alpha!
        label='Perfect calibration')
ax.set_xlabel('Nominal Coverage', fontsize=FONT_SIZES['label'])
ax.set_ylabel('Empirical Coverage', fontsize=FONT_SIZES['label'])
ax.set_title('Title', fontsize=FONT_SIZES['title'])
style_legend(ax, loc='lower right')
plt.tight_layout()
save_styled_figure(fig, 'output.svg')
```

## Workflow for New Blog Posts

1. **Create notebook**: Make a new `.qmd` file in the blog post's directory
2. **Import styling**: Add the style module import at the top
3. **Load data**: Load your CSV/data files
4. **Create plots**: Use the patterns above
5. **Save figures**: Use `save_styled_figure()` with descriptive names
6. **Update markdown**: Reference the SVG files in your blog post
7. **Update CSS**: Ensure `base.css` has the figure centering rules

## Important Notes

### Do:
- Use `plt.tight_layout()` before saving
- Use `edgecolor='none'` on histograms
- Use month names on date axes via `format_datetime_axis()`
- Use fully opaque dashed reference lines (no alpha)
- Save as SVG for crisp rendering

### Don't:
- Use transparency on main data elements (only grid and fills)
- Use colors outside the website palette
- Remove top/right spines (keep full border)
- Use different font sizes than specified
- Skip `plt.tight_layout()` (causes clipping)

## CSS Requirements

Ensure `base.css` includes:

```css
figure {
  margin: 1em auto;
  text-align: center;
}

figure img {
  display: inline-block;
  max-width: 100%;
}

figure figcaption {
  color: var(--text-color);
  text-align: justify;
  margin-top: 0.5em;
}
```

This centers figures while keeping captions left-aligned.

## Technical Details

### Minus Sign Fix
The style module sets `axes.unicode_minus: False` to prevent rendering issues with minus signs in some environments.

### Font Loading
CMU Serif should be loaded via `@font-face` in `base.css`:
```css
@font-face {
  font-family: 'CMU Serif';
  src: url('/static/fonts/cmunrm.ttf') format('truetype');
}
```

## Questions?

If creating plots for a new blog post:
1. Check existing figures in this directory for similar examples
2. Follow the color and size conventions strictly
3. When in doubt, match the style of Figures 1-7 from the ou_cox_timing_PM post
4. Ask the user about any deviations from standard patterns
