import dash
from dash import dcc, html
from dash import dash_table
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pyngrok import ngrok  # Import ngrok

# Initialize Dash app
app = dash.Dash(__name__)

# File path to your Excel file
file_path = r"E:\Dash.xlsx"  # Update this with the correct file path

# Load data from each tab
dash_1_data = pd.read_excel(file_path, sheet_name='Dash_1')  # Tab 1: Dash_1
traffic_data = pd.read_excel(file_path, sheet_name='Traffic')  # Tab 2: Traffic
dash_3_data = pd.read_excel(file_path, sheet_name='Exhibition')  # Tab 3: Dash_3

# ----------------------- Metrics for Dash_1 Tab -----------------------
# Summary Metrics for Dash_1
dash_1_summary = {
    'Total Revenue': dash_1_data['Revenue'].sum(),
    'Total Paid Sales': dash_1_data['Paid Sales'].sum(),
    'Total Ad Spend': dash_1_data['Ad Spend'].sum(),
    'Average AOV': dash_1_data['AOV'].mean(),
    'Average ROAS': dash_1_data['ROAS'].mean(),
    'Total Units Sold': dash_1_data['Units Sold'].sum(),
}

# Returning vs. New Users (Stacked Chart)
user_stack = dash_1_data.groupby('Date')[['Returning User', 'New User']].sum().reset_index()

# Ads Spend vs Paid Sales (Stacked Bar Chart)
ads_vs_paid_sales = dash_1_data.groupby('Date')[['Ad Spend', 'Paid Sales']].sum().reset_index()

# ROAS (Return on Ad Spend) Daily
roas = dash_1_data.groupby('Date')['ROAS'].mean().reset_index()

# Organic Sales vs Paid Sales (Pie Chart)
organic_paid_sales = dash_1_data[['Organic Sales', 'Paid Sales']].sum()

# AOV (Average Order Value) - Daily
aov = dash_1_data.groupby('Date')['AOV'].mean().reset_index()

# ----------------------- Metrics for Traffic Tab -----------------------
# Type sold on daily basis
type_sold_daily = traffic_data.groupby(['Date', 'Type'])['orders'].sum().reset_index()

# Pie chart for type sold in percentages
type_sold_percentage = (
    traffic_data.groupby('Type')['orders'].sum().reset_index()
)
type_sold_percentage['Percentage'] = (
    type_sold_percentage['orders'] / type_sold_percentage['orders'].sum() * 100
)

# Top 10 Cities by Total Revenue
top_10_cities = traffic_data.groupby('City')['Total Revenue'].sum().nlargest(10).reset_index()

# Source-wise Pie Chart
source_sales = traffic_data.groupby('Source')['Total Revenue'].sum().reset_index()

# ----------------------- Metrics for Dash_3 Tab -----------------------
# Add metrics and graphs for the third dashboard

# Sample metrics for Dash_3 (replace with actual metrics based on your data)
dash_3_summary = {
    'Total Orders': dash_3_data['Orders'].sum(),
    'Total Revenue': dash_3_data['Revenue'].sum(),
    'Average Order Value (AOV)': dash_3_data['AOV'].mean(),
    'Top Performing Product': dash_3_data.groupby('Popular collection')['Revenue'].sum().idxmax(),
}

# Orders by Category (Bar Chart)
orders_by_category = dash_3_data.groupby('Exhibition Name')['Orders'].sum().reset_index()

# Revenue by Category (Bar Chart)
revenue_by_category = dash_3_data.groupby('Exhibition Name')['Revenue'].sum().reset_index()

# Average Order Value (AOV) by Category (Bar Chart)
aov_by_category = dash_3_data.groupby('Exhibition Name')['AOV'].mean().reset_index()

# ----------------------- Layout of the Dash app -----------------------
app.layout = html.Div([
    html.H1("Dashboard"),

    # Dash_1 Dashboard
    html.Div([
        html.H2("Dash_1 Metrics"),

        # Summary Table
        html.H3("Summary Metrics"),
        dash_table.DataTable(
            data=[dash_1_summary],
            columns=[{"name": k, "id": k} for k in dash_1_summary.keys()],
            style_table={'overflowX': 'auto'}
        ),

        # Users: Returning vs. New Users
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=user_stack['Date'],
                        y=user_stack['Returning User'],
                        name="Returning Users",
                        text=user_stack['Returning User'],
                        textposition='auto',
                        marker=dict(color='blue'),
                        textfont=dict(size=14)
                    ),
                    go.Bar(
                        x=user_stack['Date'],
                        y=user_stack['New User'],
                        name="New Users",
                        text=user_stack['New User'],
                        textposition='auto',
                        marker=dict(color='green')
                    )
                ],
                layout=go.Layout(
                    barmode='stack',
                    title='Returning vs. New Users',
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Number of Users'}
                )
            )
        ),

        # Ads Spend vs Paid Sales
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=ads_vs_paid_sales['Date'],
                        y=ads_vs_paid_sales['Ad Spend'],
                        name="Ads Spend",
                        text=ads_vs_paid_sales['Ad Spend'],
                        textposition='auto',
                        marker=dict(color='blue'),
                        textfont=dict(size=14)
                    ),
                    go.Bar(
                        x=ads_vs_paid_sales['Date'],
                        y=ads_vs_paid_sales['Paid Sales'],
                        name="Paid Sales",
                        text=ads_vs_paid_sales['Paid Sales'],
                        textposition='auto',
                        marker=dict(color='orange')
                    )
                ],
                layout=go.Layout(
                    barmode='stack',
                    title='Ads Spend vs Paid Sales',
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Amount'}
                )
            )
        ),

        # ROAS Daily
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scatter(
                        x=roas['Date'],
                        y=roas['ROAS'],
                        mode='lines+markers+text',
                        name="ROAS",
                        text=roas['ROAS'],
                        textposition='top center'
                    )
                ],
                layout=go.Layout(
                    title='ROAS (Return on Ad Spend) - Daily',
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'ROAS'}
                )
            )
        ),

        # Organic Sales vs Paid Sales (Pie Chart)
        dcc.Graph(
            figure=px.pie(
                names=organic_paid_sales.index,
                values=organic_paid_sales,
                title="Organic vs Paid Sales"
            )
        ),

        # Average Order Value (AOV) - Daily
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scatter(
                        x=aov['Date'],
                        y=aov['AOV'],
                        mode='lines+markers+text',
                        name='AOV',
                        text=aov['AOV'],
                        textposition='top center'
                    )
                ],
                layout=go.Layout(
                    title='Average Order Value (AOV) - Daily',
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'AOV'}
                )
            )
        ),
    ]),

    # Traffic Dashboard
    html.Div([
        html.H2("Traffic Metrics"),

        # Type Sold on Daily Basis
        dcc.Graph(
            figure=px.bar(
                type_sold_daily,
                x='Date',
                y='orders',
                color='Type',
                title='Type Sold on Daily Basis',
                text='orders'
            )
        ),

        # Type Sold - Percentage (Pie Chart)
        dcc.Graph(
            figure=px.pie(
                type_sold_percentage,
                names='Type',
                values='Percentage',
                title='Type Sold (Percentage)',
                hole=0.4
            )
        ),

        # Top 10 Cities by Total Revenue
        dcc.Graph(
            figure=px.bar(
                top_10_cities,
                x='City',
                y='Total Revenue',
                title='Top 10 Cities by Total Revenue',
                text='Total Revenue'
            )
        ),

        # Source-wise Pie Chart
        dcc.Graph(
            figure=px.pie(
                source_sales,
                names='Source',
                values='Total Revenue',
                title='Source-wise Sales',
                hole=0.4
            )
        ),
    ]),

    # Dash_3 Dashboard
    html.Div([
        html.H2("Dash_3 Metrics"),

        # Summary Table
        html.H3("Summary Metrics"),
        dash_table.DataTable(
            data=[dash_3_summary],
            columns=[{"name": k, "id": k} for k in dash_3_summary.keys()],
            style_table={'overflowX': 'auto'}
        ),

        # Orders by Category
        dcc.Graph(
            figure=px.bar(
                orders_by_category,
                x='Exhibition Name',
                y='Orders',
                title='Orders by Exhibition Name',
                text='Orders'
            )
        ),

        # Revenue by Category
        dcc.Graph(
            figure=px.bar(
                revenue_by_category,
                x='Exhibition Name',
                y='Revenue',
                title='Revenue by Exhibition Name',
                text='Revenue'
            )
        ),

        # Average Order Value (AOV) by Category
        dcc.Graph(
            figure=px.bar(
                aov_by_category,
                x='Exhibition Name',
                y='AOV',
                title='AOV by Exhibition Name',
                text='AOV'
            )
        ),
    ]),

])
if __name__ == '__main__':
    app.run_server(debug=True)