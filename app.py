from datetime import datetime

from datetime import datetime

import pandas as pd

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

from config import DISPLAY_COLUMNS
from data import fetch_sales_data
from components import (
    build_filter_panel,
    build_kpi_cards,
    build_data_table,
    build_insight_cards,
)
from charts import (
    make_sales_map,
    make_sales_by_category_chart,
    make_sales_trend_chart,
    make_revenue_by_channel_chart,
    make_order_status_chart,
    make_top_products_chart,
)



app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
)

server = app.server


initial_df = fetch_sales_data()


app.layout = dbc.Container(
    fluid=True,
    className="app-container",
    children=[
        dcc.Store(id="sales-data-store", data=initial_df.to_dict("records")),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Sales Dashboard", className="page-eyebrow"),
                        html.H1("Sales Performance Overview", className="page-title"),
                        html.P(
                            "An interactive dashboard showing revenue, products, locations, channels, and order status.",
                            className="page-subtitle",
                        ),
                    ],
                    xs=12,
                    lg=8,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Refresh Data",
                            id="refresh-button",
                            color="primary",
                            className="refresh-button",
                            n_clicks=0,
                        ),
                        html.Div(
                            id="last-refresh-text",
                            className="last-refresh-text",
                        ),
                    ],
                    xs=12,
                    lg=4,
                    className="header-actions",
                ),
            ],
            className="align-items-center mb-4",
        ),

        html.Div(id="filters-section", children=build_filter_panel(initial_df)),

        html.Div(id="kpi-section", children=build_kpi_cards(initial_df)),

        html.Div(id="insights-section", children=build_insight_cards(initial_df)),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="sales-trend-chart",
                                    figure=make_sales_trend_chart(initial_df),
                                    config={"displayModeBar": False},
                                    style={"height": "420px"},
                                )
                            ]
                        ),
                        className="chart-card",
                    ),
                    xs=12,
                    lg=12,
                    className="mb-4",
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="sales-map",
                                    figure=make_sales_map(initial_df),
                                    config={"displayModeBar": False},
                                    style={"height": "460px"},
                                )
                            ]
                        ),
                        className="chart-card",
                    ),
                    xs=12,
                    lg=7,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="category-chart",
                                    figure=make_sales_by_category_chart(initial_df),
                                    config={"displayModeBar": False},
                                    style={"height": "460px"},
                                )
                            ]
                        ),
                        className="chart-card",
                    ),
                    xs=12,
                    lg=5,
                    className="mb-4",
                ),
            ],
            className="g-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="channel-chart",
                                    figure=make_revenue_by_channel_chart(initial_df),
                                    config={"displayModeBar": False},
                                    style={"height": "420px"},
                                )
                            ]
                        ),
                        className="chart-card",
                    ),
                    xs=12,
                    lg=6,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="status-chart",
                                    figure=make_order_status_chart(initial_df),
                                    config={"displayModeBar": False},
                                    style={"height": "420px"},
                                )
                            ]
                        ),
                        className="chart-card",
                    ),
                    xs=12,
                    lg=6,
                    className="mb-4",
                ),
            ],
            className="g-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id="top-products-chart",
                                    figure=make_top_products_chart(initial_df),
                                    config={"displayModeBar": False},
                                    style={"height": "520px"},
                                )
                            ]
                        ),
                        className="chart-card",
                    ),
                    xs=12,
                    className="mb-4",
                ),
            ]
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.H2("Sales Data", className="section-title"),
                            html.P(
                                "Use the filters above or the table controls below to explore the underlying records.",
                                className="section-subtitle",
                            ),
                        ],
                        className="table-header",
                    ),
                    html.Div(id="table-section", children=build_data_table(initial_df)),
                ]
            ),
            className="table-card",
        ),
    ],
)


def apply_filters(
    df,
    selected_countries,
    selected_categories,
    selected_channels,
    selected_statuses,
    selected_genders,
    start_date,
    end_date,
):
    filtered_df = df.copy()

    if selected_countries and "country" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["country"].astype(str).isin(selected_countries)
        ]

    if selected_categories and "product_cat" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["product_cat"].astype(str).isin(selected_categories)
        ]

    if selected_channels and "sales_channel" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["sales_channel"].astype(str).isin(selected_channels)
        ]

    if selected_statuses and "order_status" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["order_status"].astype(str).isin(selected_statuses)
        ]

    if selected_genders and "gender" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["gender"].astype(str).isin(selected_genders)
        ]

    if "sales_date" in filtered_df.columns:
        sales_dates = pd.to_datetime(filtered_df["sales_date"], errors="coerce")

        if start_date:
            filtered_df = filtered_df[sales_dates >= pd.to_datetime(start_date)]
            sales_dates = pd.to_datetime(filtered_df["sales_date"], errors="coerce")

        if end_date:
            filtered_df = filtered_df[sales_dates <= pd.to_datetime(end_date)]

    return filtered_df


@app.callback(
    Output("sales-data-store", "data"),
    Output("last-refresh-text", "children"),
    Input("refresh-button", "n_clicks"),
)
def refresh_data(n_clicks):
    df = fetch_sales_data()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df.to_dict("records"), f"Last refreshed: {timestamp}"

@app.callback(
    Output("kpi-section", "children"),
    Output("insights-section", "children"),
    Output("sales-trend-chart", "figure"),
    Output("sales-map", "figure"),
    Output("category-chart", "figure"),
    Output("channel-chart", "figure"),
    Output("status-chart", "figure"),
    Output("top-products-chart", "figure"),
    Output("table-section", "children"),
    Input("sales-data-store", "data"),
    Input("country-filter", "value"),
    Input("category-filter", "value"),
    Input("channel-filter", "value"),
    Input("status-filter", "value"),
    Input("gender-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
)
def update_dashboard(
    data,
    selected_countries,
    selected_categories,
    selected_channels,
    selected_statuses,
    selected_genders,
    start_date,
    end_date,
):
    df = pd.DataFrame(data)

    if df.empty:
        df = pd.DataFrame(columns=DISPLAY_COLUMNS)

    filtered_df = apply_filters(
        df,
        selected_countries,
        selected_categories,
        selected_channels,
        selected_statuses,
        selected_genders,
        start_date,
        end_date,
    )

    return (
        build_kpi_cards(filtered_df),
        build_insight_cards(filtered_df),
        make_sales_trend_chart(filtered_df),
        make_sales_map(filtered_df),
        make_sales_by_category_chart(filtered_df),
        make_revenue_by_channel_chart(filtered_df),
        make_order_status_chart(filtered_df),
        make_top_products_chart(filtered_df),
        build_data_table(filtered_df),
    )


@app.callback(
    Output("kpi-section", "children"),
    Output("sales-map", "figure"),
    Output("category-chart", "figure"),
    Output("table-section", "children"),
    Input("sales-data-store", "data"),
)
def update_dashboard(data):
    df = pd.DataFrame(data)

    if df.empty:
        df = pd.DataFrame(columns=DISPLAY_COLUMNS)

    return (
        build_kpi_cards(df),
        make_sales_map(df),
        make_sales_by_category_chart(df),
        build_data_table(df),
    )


if __name__ == "__main__":
    app.run(debug=True)
