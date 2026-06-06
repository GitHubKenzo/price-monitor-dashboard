import os
import data_loader
print("Using data_loader.py:", data_loader.__file__)
from dash.dependencies import Input, Output
from dash import Dash, html, dcc, dash_table
from data_loader import load_price_history, load_latest_prices
import plotly.express as px

app = Dash(__name__, suppress_callback_exceptions=True)

def create_price_graph():
    df = load_price_history()
    if df is None or df.empty:
        return {}
    fig = px.line(
        df,
        x="date",
        y="price",
        color="product_name",
        markers=True,
        title="Price History"
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="Product"
    )
    return fig

app.layout = html.Div([
    html.H1("Price Monitor Dashboard"),

    dcc.Tabs(id="tabs", value="tab-1", children=[
        dcc.Tab(label="価格推移グラフ", value="tab-1"),
        dcc.Tab(label="最新価格一覧", value="tab-2"),
        dcc.Tab(label="商品別ビュー", value="tab-3"),
    ]),

    html.Div(id="tab-content")
])

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_content(tab):
    if tab == "tab-1":
        return html.Div([
            html.H2("価格推移グラフ"),
            dcc.Graph(figure=create_price_graph())
        ])

    elif tab == "tab-2":
        latest_df = load_latest_prices()

        latest_df["商品名"] = latest_df.apply(
            lambda row: f'<a href="{row["url"]}" target="_blank">{row["name"]}</a>',
            axis=1
        )
        latest_df["販売元"] = latest_df["url"].apply(lambda u: u.split("/")[3])
        latest_df["価格"] = latest_df["price"]
        latest_df["最終更新日"] = latest_df["last_update"]

        latest_df = latest_df[["商品名", "販売元", "価格", "最終更新日"]]

        return html.Div([
            html.H2("最新価格一覧"),
            dash_table.DataTable(
                id="latest-table",
                columns=[
                    {"name": "商品名", "id": "商品名", "presentation": "markdown"},
                    {"name": "販売元", "id": "販売元"},
                    {"name": "価格", "id": "価格"},
                    {"name": "最終更新日", "id": "最終更新日"},
                ],
                data=latest_df.to_dict("records"),
                markdown_options={"html": True},
                style_table={"width": "90%", "margin": "0 auto"},
            )
        ])

    elif tab == "tab-3":
        df = load_price_history()
        product_list = sorted(df["product_name"].unique()) if df is not None else []

        return html.Div([
            html.H2("商品別ビュー"),

            dcc.Dropdown(
                id="product-dropdown",
                options=[{"label": p, "value": p} for p in product_list],
                value=product_list[0] if product_list else None,
                clearable=False
            ),

            dcc.Graph(id="product-graph")
        ])

@app.callback(
    Output("product-graph", "figure"),
    Input("product-dropdown", "value")
)
def update_product_graph(product_name):
    df = load_price_history()
    if df is None or df.empty or product_name is None:
        return {}

    filtered = df[df["product_name"] == product_name]

    fig = px.line(
        filtered,
        x="date",
        y="price",
        markers=True,
        title=f"{product_name} の価格推移"
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price"
    )
    return fig

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
