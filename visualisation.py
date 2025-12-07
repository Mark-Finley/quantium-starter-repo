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

# Styling tokens to keep the UI cohesive
COLORS = {
    'bg': 'linear-gradient(135deg, #f4f7fb 0%, #e8f0ff 100%)',
    'card': '#ffffff',
    'primary': '#1f77b4',
    'accent': '#ff6b6b',
    'text': '#2c3e50',
    'muted': '#6b7280',
}

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("Pink Morsel Sales Visualisation", style={
                'textAlign': 'center',
                'margin': '0',
                'color': COLORS['text'],
                'fontWeight': '700',
                'letterSpacing': '0.5px'
            }),
            html.P(
                "Track daily sales and see the impact of the January 15, 2021 price change.",
                style={
                    'textAlign': 'center',
                    'marginTop': '8px',
                    'marginBottom': '24px',
                    'color': COLORS['muted']
                }
            ),
        ], style={'padding': '16px 24px 8px 24px'}),

        html.Div([
            html.Div([
                html.Label("Filter by Region", style={
                    'fontWeight': '700',
                    'color': COLORS['text'],
                    'display': 'block',
                    'marginBottom': '8px',
                    'letterSpacing': '0.4px'
                }),
                dcc.RadioItems(
                    id='region-radio',
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': 'North', 'value': 'north'},
                        {'label': 'East', 'value': 'east'},
                        {'label': 'South', 'value': 'south'},
                        {'label': 'West', 'value': 'west'},
                    ],
                    value='all',
                    inline=True,
                    labelStyle={
                        'marginRight': '16px',
                        'padding': '6px 10px',
                        'borderRadius': '12px',
                        'border': f"1px solid {COLORS['muted']}",
                        'color': COLORS['text'],
                        'cursor': 'pointer'
                    },
                    inputStyle={
                        'marginRight': '6px'
                    },
                    style={'padding': '8px 0'}
                ),
            ], style={
                'background': COLORS['card'],
                'borderRadius': '14px',
                'padding': '16px 18px',
                'boxShadow': '0 10px 30px rgba(17, 24, 39, 0.07)',
                'border': '1px solid #e5e7eb'
            }),
        ], style={'marginBottom': '24px'}),

        html.Div([
            dcc.Graph(id='sales-chart', config={'displaylogo': False})
        ], style={
            'background': COLORS['card'],
            'borderRadius': '14px',
            'padding': '12px',
            'boxShadow': '0 16px 40px rgba(17, 24, 39, 0.08)',
            'border': '1px solid #e5e7eb'
        }),

        html.Div([
            html.P(
                "The dashed line marks the January 15, 2021 Pink Morsel price increase.",
                style={'textAlign': 'center', 'color': COLORS['muted'], 'fontSize': '13px', 'margin': '18px 0 6px 0'}
            )
        ])
    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '28px 24px 36px 24px'
    })
], style={
    'minHeight': '100vh',
    'background': COLORS['bg'],
    'fontFamily': '"Segoe UI", "Helvetica Neue", Arial, sans-serif'
})

# Callback to update the chart based on selected region
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-radio', 'value')
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
