# View Conversion Guide: Streamlit to Dash

## Quick Reference for Converting Views

This guide provides a step-by-step process for converting each Streamlit view to Dash.

## Conversion Steps

### 1. Copy the Template
```bash
cp views/view_template_dash.py views/[category]/[view_name]_dash.py
```

### 2. Analyze Original Streamlit View
Look for these Streamlit components in the original file:
- `st.title()`, `st.write()`, `st.markdown()`
- `st.columns()`, `st.metric()`
- `st.selectbox()`, `st.multiselect()`, `st.slider()`
- `st.plotly_chart()`, `st.pyplot()`
- `st.dataframe()`, `st.table()`
- `st.expander()`, `st.tabs()`

### 3. Apply Conversion Mappings

#### Headers and Text
```python
# Streamlit
st.title("📊 My Title")
st.write("Some text")
st.markdown("**Bold text**")

# Dash
html.H2("📊 My Title", className="mb-3")
html.P("Some text")
html.P(html.B("Bold text"))
```

#### Metrics
```python
# Streamlit
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Label", "Value", "Delta")

# Dash
dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H6("Label", className="text-muted mb-2"),
                html.H3("Value", className="mb-1"),
                html.P("Delta", className="text-success mb-0 small")
            ])
        ], className="metric-card shadow-sm")
    ], width=4)
])
```

#### Controls
```python
# Streamlit
selected = st.selectbox("Choose", options)
multi = st.multiselect("Select multiple", options)
value = st.slider("Adjust", 0, 100, 50)

# Dash
dcc.Dropdown(id="selector", options=[...], value=default)
dcc.Dropdown(id="multi-selector", options=[...], multi=True)
dcc.Slider(id="slider", min=0, max=100, value=50)
```

#### Charts
```python
# Streamlit
fig = px.bar(df, x="x", y="y")
st.plotly_chart(fig, use_container_width=True)

# Dash
# In layout:
dcc.Graph(id="my-chart")

# In callback:
@callback(Output("my-chart", "figure"), ...)
def update_chart(...):
    fig = px.bar(df, x="x", y="y")
    return fig
```

#### Data Tables
```python
# Streamlit
st.dataframe(df)

# Dash
dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df.columns],
    page_size=10
)
```

#### Expandable Sections
```python
# Streamlit
with st.expander("More info"):
    st.write("Details...")

# Dash
dbc.Accordion([
    dbc.AccordionItem([
        html.P("Details...")
    ], title="More info")
])
```

## Example: Converting a Simple View

### Original Streamlit View
```python
def render(data):
    st.title("📈 Historical Trends")
    
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Year", [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
    with col2:
        metric_type = st.radio("Metric", ["Adoption", "Investment", "ROI"])
    
    df = data.get("trends_data")
    if metric_type == "Adoption":
        fig = px.line(df, x="year", y="adoption_rate")
    else:
        fig = px.line(df, x="year", y=metric_type.lower())
    
    st.plotly_chart(fig, use_container_width=True)
    
    if st.checkbox("Show data"):
        st.dataframe(df)
```

### Converted Dash View
```python
def create_layout(data, persona="General"):
    return html.Div([
        html.H2("📈 Historical Trends", className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                html.Label("Year:"),
                dcc.Dropdown(
                    id="year-selector",
                    options=[{"label": y, "value": y} for y in range(2018, 2026)],
                    value=2025
                )
            ], width=6),
            dbc.Col([
                html.Label("Metric:"),
                dcc.RadioItems(
                    id="metric-selector",
                    options=[
                        {"label": "Adoption", "value": "adoption"},
                        {"label": "Investment", "value": "investment"},
                        {"label": "ROI", "value": "roi"}
                    ],
                    value="adoption"
                )
            ], width=6)
        ], className="mb-4"),
        
        dcc.Graph(id="trends-chart"),
        
        dbc.Checklist(
            id="show-data-check",
            options=[{"label": " Show data", "value": "show"}],
            value=[]
        ),
        
        html.Div(id="data-container")
    ])

@callback(
    Output("trends-chart", "figure"),
    [Input("year-selector", "value"),
     Input("metric-selector", "value")]
)
def update_chart(year, metric):
    df = get_trends_data()  # Your data logic
    if metric == "adoption":
        fig = px.line(df, x="year", y="adoption_rate")
    else:
        fig = px.line(df, x="year", y=metric)
    return fig

@callback(
    Output("data-container", "children"),
    Input("show-data-check", "value")
)
def toggle_data(show_values):
    if "show" in show_values:
        df = get_trends_data()
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns]
        )
    return html.Div()
```

## Common Patterns

### 1. Year/Time Period Filtering
Most views have year filtering. Standardize with:
```python
dcc.Dropdown(
    id="time-period-filter",
    options=[
        {"label": "All Years (2018-2025)", "value": "all"},
        {"label": "Last 3 Years", "value": "3y"},
        {"label": "Last Year", "value": "1y"}
    ],
    value="all"
)
```

### 2. Data Status Handling
Always check if data is loaded:
```python
if not data or "_metadata" not in data:
    return dbc.Alert("Loading data...", color="info")
```

### 3. Error Handling in Callbacks
Wrap chart creation in try/except:
```python
try:
    fig = create_chart(data)
    return fig
except Exception as e:
    return {
        "data": [],
        "layout": {"title": f"Error: {str(e)}"}
    }
```

### 4. Responsive Layout
Use Bootstrap grid system:
```python
dbc.Row([
    dbc.Col([...], width=12, md=6, lg=4),  # Responsive columns
])
```

## Testing Your Converted View

1. Import in the view manager:
```python
# In dash_view_manager.py
"my_view": {
    "label": "My View",
    "module": "views.category.my_view_dash",
    ...
}
```

2. Test standalone:
```python
# Create test script
from views.category.my_view_dash import create_layout
layout = create_layout({}, "General")
print("✅ View creates layout successfully")
```

3. Run the app and select your view from dropdown

## Tips for Efficient Conversion

1. **Preserve Logic**: Keep all data processing logic identical
2. **Use IDs Consistently**: `chart-type-selector`, `main-chart`, etc.
3. **Add Loading States**: Wrap charts in `dcc.Loading()`
4. **Keep Callbacks Simple**: One callback per interaction
5. **Test Incrementally**: Convert and test section by section

## Need Help?

- Check `views/adoption/adoption_rates_dash.py` for a complete example
- Review `views/view_template_dash.py` for the standard structure
- Test with `python test_dash_app.py` after conversion