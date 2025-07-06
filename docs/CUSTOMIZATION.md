# Dashboard Customization Documentation

## Overview

The AI Adoption Dashboard provides comprehensive customization features that allow users to personalize their experience with custom themes, layouts, and saved views. This enables organizations to tailor the dashboard to their specific needs and branding.

## Key Features

### 1. Custom Themes
- Create branded color schemes
- Adjust typography and spacing
- Save and share themes
- Built-in accessibility themes

### 2. Flexible Layouts
- Drag-and-drop widget positioning
- Responsive grid system
- Multiple layout templates
- Custom widget configurations

### 3. Saved Views
- Save dashboard configurations
- Quick view switching
- Share views with team
- Filter preservation

### 4. User Preferences
- Personal settings
- Default themes/layouts
- Favorite widgets
- Auto-refresh options

## Themes

### Built-in Themes

#### Light Theme (Default)
- Clean, professional appearance
- High contrast for readability
- Suitable for bright environments

#### Dark Theme
- Reduced eye strain
- Energy efficient on OLED screens
- Modern appearance

#### High Contrast
- Maximum readability
- Accessibility compliant
- Clear visual hierarchy

#### Colorblind Safe
- Optimized color palette
- Distinguishable data series
- Inclusive design

### Creating Custom Themes

```json
POST /api/customization/themes/create
{
    "name": "Corporate Brand",
    "colors": {
        "primary": "#003366",
        "secondary": "#0066CC",
        "success": "#00AA44",
        "warning": "#FFAA00",
        "error": "#CC0000",
        "background": "#FFFFFF",
        "surface": "#F8F9FA",
        "text_primary": "#212529",
        "text_secondary": "#6C757D",
        "border": "#DEE2E6"
    },
    "font_family": "Arial, sans-serif",
    "font_size_base": 14,
    "border_radius": 4,
    "spacing_unit": 8
}
```

### Theme Structure

#### Color Properties
- **primary**: Main brand color
- **secondary**: Accent color
- **success**: Positive indicators
- **warning**: Caution indicators
- **error**: Error states
- **background**: Page background
- **surface**: Card/panel background
- **text_primary**: Main text
- **text_secondary**: Supporting text
- **border**: Lines and borders

#### Typography
- **font_family**: Font stack
- **font_size_base**: Base size in pixels
- **line_height**: Text line spacing

#### Layout
- **border_radius**: Corner rounding
- **spacing_unit**: Grid spacing base

## Layouts

### Layout System

The dashboard uses a 12-column grid system:
- **Columns**: 12 (responsive)
- **Row Height**: 80px (default)
- **Spacing**: 10px between widgets

### Widget Positioning

```json
{
    "position": {
        "x": 0,      // Grid column (0-11)
        "y": 0,      // Grid row
        "w": 4,      // Width in columns
        "h": 3       // Height in rows
    }
}
```

### Pre-built Layouts

#### Financial Overview
- Key financial metrics row
- Cash flow and sensitivity charts
- Optimized for financial analysis

#### Executive Dashboard
- Executive summary
- High-level metrics
- Visual KPIs
- Risk assessment

#### Detailed Analysis
- Comprehensive metrics
- Multiple chart types
- Data tables
- Filters

### Creating Custom Layouts

```json
POST /api/customization/layouts/create
{
    "name": "Sales Dashboard",
    "type": "dashboard",
    "columns": 12,
    "widgets": [
        {
            "type": "metric",
            "title": "Total Revenue",
            "position": {"x": 0, "y": 0, "w": 3, "h": 2},
            "data_source": "revenue_total",
            "config": {
                "format": "currency",
                "show_trend": true
            }
        },
        {
            "type": "chart",
            "title": "Revenue Trend",
            "position": {"x": 3, "y": 0, "w": 9, "h": 4},
            "data_source": "revenue_monthly",
            "config": {
                "chart_type": "line",
                "show_legend": true
            }
        }
    ]
}
```

## Widgets

### Widget Types

#### 1. Chart Widget
Display data visualizations:
- Line charts
- Bar charts
- Pie charts
- Area charts
- Scatter plots

Configuration:
```json
{
    "type": "chart",
    "config": {
        "chart_type": "line",
        "show_legend": true,
        "show_grid": true,
        "animation": true
    }
}
```

#### 2. Metric Widget
Single value display:
- Current value
- Trend indicator
- Comparison to target
- Sparkline

Configuration:
```json
{
    "type": "metric",
    "config": {
        "format": "currency",
        "show_trend": true,
        "comparison": "previous_period"
    }
}
```

#### 3. Table Widget
Tabular data display:
- Sortable columns
- Filterable
- Pagination
- Export options

#### 4. Text Widget
Rich text content:
- Markdown support
- HTML templates
- Dynamic content

#### 5. Filter Widget
Interactive controls:
- Date ranges
- Dropdowns
- Multi-select
- Search

#### 6. Calculator Widget
Interactive calculations:
- NPV calculator
- ROI calculator
- Custom formulas

### Widget Configuration

Common properties:
```json
{
    "id": "unique-id",
    "type": "chart",
    "title": "Widget Title",
    "position": {"x": 0, "y": 0, "w": 4, "h": 3},
    "data_source": "api_endpoint",
    "refresh_interval": 300,  // seconds
    "visible": true,
    "config": {
        // Type-specific configuration
    }
}
```

## Saved Views

### Creating Saved Views

Save complete dashboard state:
```json
POST /api/customization/views/save
{
    "name": "Q4 Financial Analysis",
    "description": "End of year financial review",
    "layout_id": "layout-financial",
    "theme_id": "theme-dark",
    "filters": {
        "date_range": "2024-Q4",
        "department": "all",
        "metric_type": "actual"
    },
    "is_public": false,
    "tags": ["finance", "quarterly", "executive"]
}
```

### View Properties
- **name**: Display name
- **description**: Detailed description
- **layout_id**: Associated layout
- **theme_id**: Associated theme
- **filters**: Active filters
- **is_public**: Share with others
- **is_default**: Load on startup
- **tags**: Categorization

### Managing Views

#### List Views
```http
GET /api/customization/views
```

#### Apply View
```http
POST /api/customization/views/apply
{
    "view_id": "view-123"
}
```

#### Delete View
```http
DELETE /api/customization/views/delete
{
    "view_id": "view-123"
}
```

## User Preferences

### Preference Settings

```json
{
    "default_theme_id": "theme-dark",
    "default_layout_id": "layout-executive",
    "favorite_widgets": ["npv-calc", "roi-chart"],
    "settings": {
        "auto_refresh": true,
        "refresh_interval": 300,
        "show_tooltips": true,
        "animation_speed": "normal",
        "number_format": "en-US",
        "date_format": "MM/DD/YYYY",
        "timezone": "America/New_York"
    }
}
```

### Update Preferences
```http
PUT /api/customization/preferences/update
{
    "default_theme_id": "theme-custom-123",
    "settings": {
        "auto_refresh": false
    }
}
```

## Import/Export

### Export Configuration
Export all customizations:
```http
GET /api/customization/export
```

Response includes:
- Custom themes
- Custom layouts
- Saved views
- Preferences

### Import Configuration
```http
POST /api/customization/import
{
    "configuration": {
        // Exported configuration object
    }
}
```

## Best Practices

### Theme Design
1. **Contrast**: Ensure sufficient contrast (WCAG AA)
2. **Consistency**: Use consistent color meanings
3. **Branding**: Align with corporate identity
4. **Accessibility**: Test with various vision conditions

### Layout Design
1. **Information Hierarchy**: Most important widgets first
2. **Visual Flow**: Natural reading patterns
3. **Responsiveness**: Test on various screen sizes
4. **Performance**: Limit widgets per view

### Widget Selection
1. **Purpose**: Each widget should have clear purpose
2. **Data Density**: Balance detail with clarity
3. **Interactivity**: Enable where beneficial
4. **Loading**: Consider data fetch times

## API Reference

### Endpoints

#### Themes
- `GET /api/customization/themes` - List themes
- `POST /api/customization/themes/create` - Create theme

#### Layouts
- `GET /api/customization/layouts` - List layouts
- `POST /api/customization/layouts/create` - Create layout

#### Views
- `GET /api/customization/views` - List saved views
- `POST /api/customization/views/save` - Save view
- `POST /api/customization/views/apply` - Apply view
- `DELETE /api/customization/views/delete` - Delete view

#### Preferences
- `GET /api/customization/preferences` - Get preferences
- `PUT /api/customization/preferences/update` - Update preferences

#### Import/Export
- `GET /api/customization/export` - Export configuration
- `POST /api/customization/import` - Import configuration

#### Widget Types
- `GET /api/customization/widgets/types` - List widget types

## Examples

### Example: Corporate Dashboard

```python
# Create corporate theme
theme = create_theme({
    "name": "Corporate",
    "colors": {
        "primary": "#1B5E20",
        "secondary": "#4CAF50",
        "background": "#FAFAFA"
    }
})

# Create executive layout
layout = create_layout({
    "name": "Executive Overview",
    "widgets": [
        {
            "type": "text",
            "title": "Executive Summary",
            "position": {"x": 0, "y": 0, "w": 12, "h": 2}
        },
        {
            "type": "metric",
            "title": "Total ROI",
            "position": {"x": 0, "y": 2, "w": 3, "h": 2}
        }
        # ... more widgets
    ]
})

# Save as default view
view = save_view({
    "name": "Executive Default",
    "layout_id": layout.id,
    "theme_id": theme.id,
    "is_default": true
})
```

### Example: Department View

```javascript
// Apply department-specific view
const response = await fetch('/api/customization/views/apply', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        view_id: 'view-finance-dept'
    })
});

const config = await response.json();
// Dashboard updates with new theme, layout, and filters
```

## Troubleshooting

### Common Issues

#### Theme Not Applying
- Check theme ID validity
- Verify color format (#RRGGBB)
- Clear browser cache

#### Layout Errors
- Validate widget positions
- Check for overlapping widgets
- Ensure grid boundaries

#### View Not Saving
- Verify required fields
- Check permissions
- Validate filter format

#### Performance Issues
- Limit widgets per view
- Optimize data sources
- Use appropriate refresh intervals

## Future Enhancements

1. **Theme Marketplace**
   - Share themes publicly
   - Download community themes
   - Theme ratings

2. **Advanced Layouts**
   - Nested containers
   - Responsive breakpoints
   - Layout templates

3. **Widget Builder**
   - Custom widget creation
   - Widget marketplace
   - Plugin system

4. **Collaboration**
   - Real-time view sharing
   - Commenting on widgets
   - Change notifications