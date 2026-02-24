import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# Load data
conn = sqlite3.connect("health.db")
df = pd.read_sql("SELECT * FROM health", conn)
conn.close()

# Clean numeric columns
numeric_cols = [
    'birth_rate', 'general_fertility_rate', 'low_birth_weight',
    'prenatal_care_beginning_in_first_trimester', 'preterm_births',
    'teen_birth_rate', 'assault_homicide', 'breast_cancer_in_females',
    'cancer_all_sites', 'colorectal_cancer', 'diabetes_related',
    'firearm_related', 'infant_mortality_rate', 'lung_cancer',
    'prostate_cancer_in_males', 'stroke_cerebrovascular_disease',
    'childhood_blood_lead_level_screening', 'childhood_lead_poisoning',
    'gonorrhea_in_females', 'gonorrhea_in_males', 'tuberculosis',
    'below_poverty_level', 'crowded_housing', 'dependency',
    'no_high_school_diploma', 'per_capita_income', 'unemployment'
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

indicator_options = [
    {'label': col.replace('_', ' ').title(), 'value': col}
    for col in numeric_cols
]

app = dash.Dash(__name__)
server = app.server
app.title = "Chicago Community Health Dashboard"

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Chicago Community Health Dashboard",
                style={'color': 'white', 'margin': '0', 'fontSize': '28px'}),
        html.P("Public health indicators across 77 Chicago community areas",
               style={'color': '#ccc', 'margin': '5px 0 0 0'})
    ], style={
        'backgroundColor': '#1a1a2e',
        'padding': '30px 40px',
        'marginBottom': '30px'
    }),

    # KPI Cards
    html.Div(id='kpi-cards', style={
        'display': 'flex',
        'gap': '20px',
        'padding': '0 40px',
        'marginBottom': '30px',
        'flexWrap': 'wrap'
    }),

    # Controls
    html.Div([
        html.Div([
            html.Label("Select Health Indicator", style={'fontWeight': 'bold', 'marginBottom': '8px', 'display': 'block'}),
            dcc.Dropdown(
                id='indicator-dropdown',
                options=indicator_options,
                value='diabetes_related',
                clearable=False,
                style={'width': '400px'}
            )
        ]),
    ], style={'padding': '0 40px', 'marginBottom': '20px'}),

    # Charts Row 1
    html.Div([
        html.Div([
            dcc.Graph(id='bar-chart')
        ], style={'flex': '2', 'backgroundColor': 'white', 'borderRadius': '8px', 'padding': '10px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'}),

        html.Div([
            dcc.Graph(id='scatter-chart')
        ], style={'flex': '1', 'backgroundColor': 'white', 'borderRadius': '8px', 'padding': '10px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'})
    ], style={'display': 'flex', 'gap': '20px', 'padding': '0 40px', 'marginBottom': '20px'}),

    # Charts Row 2
    html.Div([
        html.Div([
            dcc.Graph(id='poverty-chart')
        ], style={'flex': '1', 'backgroundColor': 'white', 'borderRadius': '8px', 'padding': '10px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'}),

        html.Div([
            dcc.Graph(id='income-chart')
        ], style={'flex': '1', 'backgroundColor': 'white', 'borderRadius': '8px', 'padding': '10px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'})
    ], style={'display': 'flex', 'gap': '20px', 'padding': '0 40px', 'marginBottom': '40px'})

], style={'backgroundColor': '#f5f5f5', 'minHeight': '100vh', 'fontFamily': 'Arial, sans-serif'})


@app.callback(
    Output('kpi-cards', 'children'),
    Output('bar-chart', 'figure'),
    Output('scatter-chart', 'figure'),
    Output('poverty-chart', 'figure'),
    Output('income-chart', 'figure'),
    Input('indicator-dropdown', 'value')
)
def update_dashboard(indicator):
    label = indicator.replace('_', ' ').title()
    valid = df[indicator].dropna()

    # KPI Cards
    kpis = [
        ("Avg " + label, f"{valid.mean():.1f}", "#e74c3c"),
        ("Max " + label, f"{valid.max():.1f} ({df.loc[df[indicator].idxmax(), 'community_area_name']})", "#e67e22"),
        ("Min " + label, f"{valid.min():.1f} ({df.loc[df[indicator].idxmin(), 'community_area_name']})", "#27ae60"),
        ("Communities Tracked", str(len(valid)), "#2980b9"),
    ]
    cards = []
    for title, value, color in kpis:
        cards.append(html.Div([
            html.P(title, style={'margin': '0', 'fontSize': '13px', 'color': '#666'}),
            html.H3(value, style={'margin': '5px 0 0 0', 'color': color, 'fontSize': '18px'})
        ], style={
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '8px',
            'flex': '1',
            'minWidth': '200px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
            'borderLeft': f'4px solid {color}'
        }))

    # Bar chart - top 15 communities
    top15 = df.nlargest(15, indicator)[['community_area_name', indicator]].dropna()
    bar_fig = px.bar(
        top15, x=indicator, y='community_area_name',
        orientation='h',
        title=f"Top 15 Communities — {label}",
        color=indicator,
        color_continuous_scale='Reds',
        labels={indicator: label, 'community_area_name': 'Community'}
    )
    bar_fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)

    # Scatter - indicator vs poverty
    scatter_fig = px.scatter(
        df, x='below_poverty_level', y=indicator,
        hover_name='community_area_name',
        title=f"{label} vs Poverty Rate",
        trendline='ols',
        labels={'below_poverty_level': 'Below Poverty Level (%)', indicator: label},
        color=indicator,
        color_continuous_scale='Blues'
    )

    # Poverty distribution
    poverty_fig = px.histogram(
        df, x='below_poverty_level',
        title="Poverty Rate Distribution Across Communities",
        nbins=20,
        color_discrete_sequence=['#3498db'],
        labels={'below_poverty_level': 'Below Poverty Level (%)'}
    )

    # Per capita income vs selected indicator
    income_fig = px.scatter(
        df, x='per_capita_income', y=indicator,
        hover_name='community_area_name',
        title=f"{label} vs Per Capita Income",
        trendline='ols',
        labels={'per_capita_income': 'Per Capita Income ($)', indicator: label},
        color='per_capita_income',
        color_continuous_scale='Greens'
    )

    return cards, bar_fig, scatter_fig, poverty_fig, income_fig


if __name__ == '__main__':
    app.run(debug=True)
