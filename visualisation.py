import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

# Load the formatted sales data
df = pd.read_csv('data/formatted_sales_data.csv')

# Strip whitespace from column names
df.columns = df.columns.str.strip()
df['region'] = df['region'].str.strip()

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'].str.strip())

# Sort by date
df = df.sort_values('date')

# Calculate total sales by date (sum across all regions)
daily_sales = df.groupby('date')['sales'].sum().reset_index()
daily_sales = daily_sales.sort_values('date')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.H1("Pink Morsel Sales Visualisation", style={
            'textAlign': 'center',
            'marginBottom': 30,
            'marginTop': 20,
            'color': '#333'
        })
    ]),
    
    html.Div([
        html.Div([
            html.Label("Select Region:", style={'fontWeight': 'bold', 'marginRight': 10}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[
                    {'label': 'All Regions', 'value': 'all'},
                    {'label': 'North', 'value': 'north'},
                    {'label': 'South', 'value': 'south'},
                    {'label': 'East', 'value': 'east'},
                    {'label': 'West', 'value': 'west'},
                ],
                value='all',
                style={'width': '200px'}
            )
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': 20, 'marginLeft': 20}),
    ]),
    
    html.Div([
        dcc.Graph(id='sales-chart')
    ], style={'marginBottom': 30}),
    
    html.Div([
        html.P(
            "Note: The vertical line at January 15, 2021 indicates the date of the Pink Morsel price increase.",
            style={'textAlign': 'center', 'color': '#666', 'fontSize': 12, 'marginBottom': 10}
        )
    ])
], style={
    'fontFamily': 'Arial, sans-serif',
    'maxWidth': '1200px',
    'margin': '0 auto',
    'padding': '20px'
})

# Callback to update the chart based on selected region
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-dropdown', 'value')
)
def update_chart(selected_region):
    try:
        # Filter data based on selected region
        if selected_region == 'all':
            plot_data = daily_sales.copy()
        else:
            filtered_df = df[df['region'].str.strip() == selected_region.lower()]
            plot_data = filtered_df.groupby('date')['sales'].sum().reset_index()
            plot_data = plot_data.sort_values('date')
        
        # Create the figure
        fig = go.Figure()
        
        # Add the line chart
        fig.add_trace(go.Scatter(
            x=plot_data['date'],
            y=plot_data['sales'],
            mode='lines',
            name='Daily Sales',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        
        # Add a vertical line for the price increase date using shapes instead of add_vline
        price_increase_date = '2021-01-15'
        fig.add_shape(
            type="line",
            x0=price_increase_date, x1=price_increase_date,
            y0=0, y1=1,
            yref="paper",
            line=dict(color="red", width=2, dash="dash"),
        )
        
        fig.add_annotation(
            x=price_increase_date,
            y=1,
            yref="paper",
            text="Price Increase",
            showarrow=False,
            yshift=10,
            font=dict(color="red")
        )
        
        # Update layout
        fig.update_layout(
            title=f"Pink Morsel Sales - {'All Regions' if selected_region == 'all' else selected_region.title()}",
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            hovermode='x unified',
            template='plotly_white',
            height=500,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig
    except Exception as e:
        # Return an error figure if something goes wrong
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

if __name__ == '__main__':
    app.run(debug=True)
