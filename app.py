from datetime import datetime

import pandas as pd

from dash import Dash, dcc, html, Input, Output, State, ctx, no_update
import dash_bootstrap_components as dbc

from config import DISPLAY_COLUMNS
from data import (
    fetch_sales_data,
    insert_sale_record,
    update_sale_record,
    delete_sale_record,
)
from components import (
    build_filter_panel,
    build_kpi_cards,
    build_data_table,
    build_insight_cards,
    build_data_management_tab,
    build_management_table,
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
                        html.Img(
                                src="/assets/logo_v1.png",
                                className="page-logo",
                                alt="DataChum logo",
                            ),
                        html.P(
                            "We turn your data into clear, actionable insights — helping you spot trends, understand performance, and make better decisions faster.",
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

        dbc.Tabs(
            id="main-tabs",
            active_tab="insights-tab",
            className="dashboard-tabs mb-4",
            children=[
                dbc.Tab(
                    label="Insights",
                    tab_id="insights-tab",
                    children=[
                        html.Div(
                            [
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
                                            html.H2("Sales Data", className="section-title"),
                                            html.P(
                                                "Use the filters above or the table controls below to explore the underlying records.",
                                                className="section-subtitle",
                                            ),
                                            html.Div(id="table-section", children=build_data_table(initial_df)),
                                        ]
                                    ),
                                    className="table-card",
                                ),
                            ],
                            className="tab-content-wrapper",
                        )
                    ],
                ),

                dbc.Tab(
                    label="Manage Data",
                    tab_id="manage-data-tab",
                    children=[
                        html.Div(
                            id="manage-data-tab-content",
                            children=build_data_management_tab(initial_df),
                            className="tab-content-wrapper",
                        )
                    ],
                ),
            ],
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
    Output("management-message", "children"),
    Input("refresh-button", "n_clicks"),
    Input("add-sale-button", "n_clicks"),
    Input("save-edits-button", "n_clicks"),
    Input("delete-selected-button", "n_clicks"),
    State("add-first-name", "value"),
    State("add-last-name", "value"),
    State("add-email", "value"),
    State("add-gender", "value"),
    State("add-product-cat", "value"),
    State("add-product-name", "value"),
    State("add-product-price", "value"),
    State("add-country", "value"),
    State("add-sales-date", "date"),
    State("add-city", "value"),
    State("add-sales-channel", "value"),
    State("add-order-status", "value"),
    State("management-table", "data"),
    State("management-table", "selected_rows"),
    prevent_initial_call=True,
)
def handle_data_actions(
    refresh_clicks,
    add_clicks,
    save_clicks,
    delete_clicks,
    first_name,
    last_name,
    email,
    gender,
    product_cat,
    product_name,
    product_price,
    country,
    sales_date,
    city,
    sales_channel,
    order_status,
    management_table_data,
    selected_rows,
):
    triggered_id = ctx.triggered_id

    try:
        if triggered_id == "refresh-button":
            df = fetch_sales_data()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return (
                df.to_dict("records"),
                f"Last refreshed: {timestamp}",
                "",
            )

        if triggered_id == "add-sale-button":
            required_fields = {
                "First name": first_name,
                "Last name": last_name,
                "Email": email,
                "Product category": product_cat,
                "Product name": product_name,
                "Product price": product_price,
                "Country": country,
                "Sales date": sales_date,
                "Sales channel": sales_channel,
                "Order status": order_status,
            }

            missing_fields = [
                label for label, value in required_fields.items()
                if value in [None, ""]
            ]

            if missing_fields:
                return (
                    no_update,
                    no_update,
                    dbc.Alert(
                        f"Please complete these required fields: {', '.join(missing_fields)}.",
                        color="warning",
                    ),
                )

            new_record = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "gender": gender,
                "product_cat": product_cat,
                "product_name": product_name,
                "product_price": product_price,
                "country": country,
                "sales_date": sales_date,
                "city": city,
                "sales_channel": sales_channel,
                "order_status": order_status,
            }

            insert_sale_record(new_record)

            df = fetch_sales_data()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return (
                df.to_dict("records"),
                f"Last refreshed: {timestamp}",
                dbc.Alert("Record added successfully.", color="success"),
            )

        if triggered_id == "save-edits-button":
            if not management_table_data:
                return (
                    no_update,
                    no_update,
                    dbc.Alert("There are no records to update.", color="warning"),
                )

            updated_count = 0

            for row in management_table_data:
                record_id = row.get("id")

                if record_id is None:
                    continue

                updates = {
                    "first_name": row.get("first_name"),
                    "last_name": row.get("last_name"),
                    "email": row.get("email"),
                    "gender": row.get("gender"),
                    "product_cat": row.get("product_cat"),
                    "product_name": row.get("product_name"),
                    "product_price": row.get("product_price"),
                    "country": row.get("country"),
                    "sales_date": row.get("sales_date"),
                    "city": row.get("city"),
                    "sales_channel": row.get("sales_channel"),
                    "order_status": row.get("order_status"),
                }

                update_sale_record(record_id, updates)
                updated_count += 1

            df = fetch_sales_data()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return (
                df.to_dict("records"),
                f"Last refreshed: {timestamp}",
                dbc.Alert(f"Saved edits for {updated_count:,} records.", color="success"),
            )

        if triggered_id == "delete-selected-button":
            if not selected_rows:
                return (
                    no_update,
                    no_update,
                    dbc.Alert("Please select at least one row to delete.", color="warning"),
                )

            if not management_table_data:
                return (
                    no_update,
                    no_update,
                    dbc.Alert("There are no records available to delete.", color="warning"),
                )

            deleted_count = 0

            for row_index in selected_rows:
                if row_index >= len(management_table_data):
                    continue

                row = management_table_data[row_index]
                record_id = row.get("id")

                if record_id is None:
                    continue

                delete_sale_record(record_id)
                deleted_count += 1

            df = fetch_sales_data()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return (
                df.to_dict("records"),
                f"Last refreshed: {timestamp}",
                dbc.Alert(f"Deleted {deleted_count:,} selected records.", color="success"),
            )

        return no_update, no_update, no_update

    except Exception as error:
        return (
            no_update,
            no_update,
            dbc.Alert(f"Something went wrong: {error}", color="danger"),
        )


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
