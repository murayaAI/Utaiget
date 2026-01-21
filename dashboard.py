import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Hello from Dashboard"),
    html.P("This is your test dashboard running successfully.")
])
