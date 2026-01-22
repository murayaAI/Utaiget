import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from db.database import SessionLocal
from db.models import Package, Seller

SELLER_ID = 1  # Change this for each seller

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = f"Seller Dashboard - Seller {SELLER_ID}"

# -----------------------------
# Database Query Functions
# -----------------------------
def get_packages():
    """Return packages for this seller as a DataFrame"""
    with SessionLocal() as db:
        packages = db.query(Package).filter_by(seller_id=SELLER_ID).all()
        return pd.DataFrame([{
            "Package ID": p.id,
            "Buyer ID": p.buyer_id,
            "Courier ID": p.courier_id,
            "FC ID": p.fc_id,
            "Status": p.status
        } for p in packages])

def get_wallet():
    """Return wallet balance for this seller"""
    with SessionLocal() as db:
        seller = db.get(Seller, SELLER_ID)
        return seller.wallet if seller else 0

# -----------------------------
# Layout
# -----------------------------
app.layout = dbc.Container([
    html.H2(f"Seller Dashboard - Seller {SELLER_ID}", className="my-3"),
    dbc.Alert(id="wallet-div", color="success"),
    dcc.Interval(id="interval", interval=5000, n_intervals=0),
    html.H4("Your Packages"),
    html.Div(id="table-div")
], fluid=True)

# -----------------------------
# Callbacks
# -----------------------------
@app.callback(
    [dash.Output("table-div", "children"),
     dash.Output("wallet-div", "children")],
    [dash.Input("interval", "n_intervals")]
)
def update_dashboard(n):
    df = get_packages()
    wallet = get_wallet()

    if df.empty:
        table = html.Div("No packages yet.")
    else:
        table = dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_data_conditional=[
                {
                    "if": {"filter_query": f'{{Status}} = "{status}"'},
                    "backgroundColor": color
                } for status, color in {
                    "created": "lightgray",
                    "assigned": "lightblue",
                    "delivered": "lightgreen"
                }.items()
            ],
            style_header={"backgroundColor": "purple", "color": "white", "fontWeight": "bold"},
            style_cell={"textAlign": "center", "padding": "5px"},
            page_size=10
        )

    return table, f"Wallet: KES {wallet}"

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    app.run_server(debug=True, port=8051, use_reloader=False)
