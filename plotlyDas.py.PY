import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the SpaceX launch data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Extract unique launch site names
launch_sites = spacex_df['Launch Site'].unique()

# Calculate min and max payload values
min_payload = spacex_df['PayloadMass'].min()
max_payload = spacex_df['PayloadMass'].max()

# Create the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',
        placeholder="Select a launch site",
        searchable=True
    ),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={min_payload: str(min_payload), max_payload: str(max_payload)},
        value=[min_payload, max_payload]
    ),
    dcc.Graph(id='success-pie-chart'),
    dcc.Graph(id='success-payload-scatter-chart')
])

# Callback function for success-pie-chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_pie_chart(selected_site, payload_range):
    # ... (same as before)

# Callback function for success-payload-scatter-chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_data = spacex_df[(spacex_df['PayloadMass'] >= payload_range[0]) & (spacex_df['PayloadMass'] <= payload_range[1])]
        title = f'Success Payload Scatter Plot for All Sites ({payload_range[0]} - {payload_range[1]} Kg Payload)'
    else:
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        filtered_data = site_data[(site_data['PayloadMass'] >= payload_range[0]) & (site_data['PayloadMass'] <= payload_range[1])]
        title = f'Success Payload Scatter Plot for {selected_site} ({payload_range[0]} - {payload_range[1]} Kg Payload)'
    
    fig = px.scatter(
        filtered_data,
        x='PayloadMass',
        y='Class',
        color='Booster Version Category',
        title=title,
        labels={'PayloadMass': 'Payload Mass (kg)', 'Class': 'Class'}
    )
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

