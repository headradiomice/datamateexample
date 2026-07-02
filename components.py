import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table, html, dcc



from config import TABLE_COLUMNS


def build_kpi_cards(df):
    total_orders = len(df)

    total_revenue = 0
    if "product_price" in df.columns:
        total_revenue = df["product_price"].fillna(0).sum()

    avg_order_value = total_revenue / total_orders if total_orders else 0

    top_country = "N/A"
    if not df.empty and "country" in df.columns and "product_price" in df.columns:
        country_revenue = df.groupby("country")["product_price"].sum()
        if not country_revenue.empty:
            top_country = country_revenue.idxmax()

    top_category = "N/A"
    if not df.empty and "product_cat" in df.columns and "product_price" in df.columns:
        category_revenue = df.groupby("product_cat")["product_price"].sum()
        if not category_revenue.empty:
            top_category = category_revenue.idxmax()

    completion_rate = 0
    if total_orders and "order_status" in df.columns:
        completed_orders = (
            df["order_status"]
            .astype(str)
            .str.lower()
            .eq("completed")
            .sum()
        )
        completion_rate = completed_orders / total_orders

    cards = [
        {
            "label": "Total Revenue",
            "value": f"${total_revenue:,.0f}",
            "icon": "💰",
        },
        {
            "label": "Total Orders",
            "value": f"{total_orders:,}",
            "icon": "📦",
        },
        {
            "label": "Avg Order Value",
            "value": f"${avg_order_value:,.2f}",
            "icon": "🧾",
        },
        {
            "label": "Top Country",
            "value": str(top_country),
            "icon": "🌍",
        },
        {
            "label": "Top Category",
            "value": str(top_category),
            "icon": "🏆",
        },
        {
            "label": "Completion Rate",
            "value": f"{completion_rate:.1%}",
            "icon": "✅",
        },
    ]

    return dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(card["icon"], className="kpi-icon"),
                            html.Div(card["label"], className="kpi-label"),
                            html.Div(card["value"], className="kpi-value"),
                        ]
                    ),
                    className="kpi-card",
                ),
                xs=12,
                sm=6,
                lg=2,
                className="mb-3",
            )
            for card in cards
        ],
        className="g-3",
    )


def build_data_table(df):
    if df.empty:
        df = pd.DataFrame(columns=TABLE_COLUMNS)

    return dash_table.DataTable(
        id="sales-table",
        data=df.to_dict("records"),
        columns=[
            {
                "name": col.replace("_", " ").title(),
                "id": col,
                "type": "numeric" if col == "product_price" else "text",
            }
            for col in df.columns
        ],
        page_size=25,
        sort_action="native",
        filter_action="native",
        fixed_rows={"headers": True},
        style_table={
            "overflowX": "auto",
            "overflowY": "auto",
            "maxHeight": "620px",
            "border": "1px solid #e5e7eb",
            "borderRadius": "14px",
        },
        style_header={
            "backgroundColor": "#0f172a",
            "color": "white",
            "fontWeight": "700",
            "border": "none",
            "fontSize": "13px",
            "textTransform": "uppercase",
            "letterSpacing": "0.04em",
        },
        style_cell={
            "fontFamily": "Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "fontSize": "14px",
            "padding": "12px",
            "border": "1px solid #f1f5f9",
            "textAlign": "left",
            "minWidth": "120px",
            "maxWidth": "260px",
            "whiteSpace": "normal",
        },
        style_data={
            "backgroundColor": "white",
            "color": "#111827",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#f8fafc",
            },
            {
                "if": {"state": "active"},
                "backgroundColor": "#e0f2fe",
                "border": "1px solid #0284c7",
            },
        ],
        style_filter={
            "backgroundColor": "#f8fafc",
            "border": "1px solid #e5e7eb",
        },
    )

def make_dropdown_options(df, column):
    if df.empty or column not in df.columns:
        return []

    values = (
        df[column]
        .dropna()
        .astype(str)
        .sort_values()
        .unique()
        .tolist()
    )

    return [{"label": value, "value": value} for value in values]


def build_filter_panel(df):
    date_min = None
    date_max = None

    if not df.empty and "sales_date" in df.columns:
        dates = pd.to_datetime(df["sales_date"], errors="coerce").dropna()

        if not dates.empty:
            date_min = dates.min().date()
            date_max = dates.max().date()

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.H2("Filters", className="section-title"),
                        html.P(
                            "Use these filters to explore different markets, channels, products, and order statuses.",
                            className="section-subtitle",
                        ),
                    ],
                    className="mb-3",
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Date Range", className="filter-label"),
                                dcc.DatePickerRange(
                                    id="date-filter",
                                    min_date_allowed=date_min,
                                    max_date_allowed=date_max,
                                    start_date=date_min,
                                    end_date=date_max,
                                    display_format="YYYY-MM-DD",
                                    clearable=True,
                                    className="date-picker",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),

                        dbc.Col(
                            [
                                html.Label("Country", className="filter-label"),
                                dcc.Dropdown(
                                    id="country-filter",
                                    options=make_dropdown_options(df, "country"),
                                    value=[],
                                    multi=True,
                                    placeholder="All countries",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),

                        dbc.Col(
                            [
                                html.Label("Product Category", className="filter-label"),
                                dcc.Dropdown(
                                    id="category-filter",
                                    options=make_dropdown_options(df, "product_cat"),
                                    value=[],
                                    multi=True,
                                    placeholder="All categories",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),

                        dbc.Col(
                            [
                                html.Label("Sales Channel", className="filter-label"),
                                dcc.Dropdown(
                                    id="channel-filter",
                                    options=make_dropdown_options(df, "sales_channel"),
                                    value=[],
                                    multi=True,
                                    placeholder="All channels",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),

                        dbc.Col(
                            [
                                html.Label("Order Status", className="filter-label"),
                                dcc.Dropdown(
                                    id="status-filter",
                                    options=make_dropdown_options(df, "order_status"),
                                    value=[],
                                    multi=True,
                                    placeholder="All statuses",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),

                        dbc.Col(
                            [
                                html.Label("Gender", className="filter-label"),
                                dcc.Dropdown(
                                    id="gender-filter",
                                    options=make_dropdown_options(df, "gender"),
                                    value=[],
                                    multi=True,
                                    placeholder="All genders",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                    ],
                    className="g-3",
                ),
            ]
        ),
        className="filter-card mb-4",
    )

def build_insight_cards(df):
    if df.empty:
        insights = [
            "No data is available for the selected filters.",
            "Try changing or clearing the filters to see more results.",
        ]
    else:
        insights = []

        total_orders = len(df)

        if "product_price" in df.columns:
            total_revenue = df["product_price"].fillna(0).sum()
            avg_order_value = total_revenue / total_orders if total_orders else 0

            insights.append(
                f"The selected data contains {total_orders:,} orders with total revenue of ${total_revenue:,.0f}."
            )

            insights.append(
                f"The average order value is ${avg_order_value:,.2f}."
            )

        if "product_cat" in df.columns and "product_price" in df.columns:
            category_revenue = df.groupby("product_cat")["product_price"].sum().sort_values(ascending=False)

            if not category_revenue.empty:
                top_category = category_revenue.index[0]
                top_category_revenue = category_revenue.iloc[0]

                insights.append(
                    f"The highest revenue product category is {top_category}, generating ${top_category_revenue:,.0f}."
                )

        if "country" in df.columns and "product_price" in df.columns:
            country_revenue = df.groupby("country")["product_price"].sum().sort_values(ascending=False)

            if not country_revenue.empty:
                top_country = country_revenue.index[0]
                top_country_revenue = country_revenue.iloc[0]

                insights.append(
                    f"The top country by revenue is {top_country}, generating ${top_country_revenue:,.0f}."
                )

        if "sales_channel" in df.columns and "product_price" in df.columns:
            channel_revenue = df.groupby("sales_channel")["product_price"].sum().sort_values(ascending=False)

            if not channel_revenue.empty:
                top_channel = channel_revenue.index[0]
                top_channel_revenue = channel_revenue.iloc[0]

                insights.append(
                    f"The strongest sales channel is {top_channel}, with ${top_channel_revenue:,.0f} in revenue."
                )

        if "order_status" in df.columns:
            completed_rate = (
                df["order_status"]
                .astype(str)
                .str.lower()
                .eq("completed")
                .mean()
            )

            insights.append(
                f"{completed_rate:.1%} of orders in the current view are marked as completed."
            )

    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Key Insights", className="section-title"),
                html.P(
                    "Automatically generated summary points based on the selected data.",
                    className="section-subtitle",
                ),
                html.Ul(
                    [html.Li(insight, className="insight-item") for insight in insights],
                    className="insight-list",
                ),
            ]
        ),
        className="insight-card mb-4",
    )

def build_add_sale_form(df):
    """
    Form used to add a new sale record.
    """

    def options_from_column(column, fallback=None):
        fallback = fallback or []

        if df.empty or column not in df.columns:
            values = fallback
        else:
            values = (
                df[column]
                .dropna()
                .astype(str)
                .sort_values()
                .unique()
                .tolist()
            )

            values = sorted(set(values + fallback))

        return [{"label": value, "value": value} for value in values]

    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Add New Sale", className="section-title"),
                html.P(
                    "Use this form to add a new sales record to the database.",
                    className="section-subtitle",
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("First Name", className="filter-label"),
                                dbc.Input(id="add-first-name", type="text", placeholder="First name"),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            [
                                html.Label("Last Name", className="filter-label"),
                                dbc.Input(id="add-last-name", type="text", placeholder="Last name"),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            [
                                html.Label("Email", className="filter-label"),
                                dbc.Input(id="add-email", type="email", placeholder="email@example.com"),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            [
                                html.Label("Gender", className="filter-label"),
                                dcc.Dropdown(
                                    id="add-gender",
                                    options=options_from_column(
                                        "gender",
                                        fallback=["Female", "Male", "Other"],
                                    ),
                                    placeholder="Select gender",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                    ],
                    className="g-3",
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Product Category", className="filter-label"),
                                dcc.Dropdown(
                                    id="add-product-cat",
                                    options=options_from_column("product_cat"),
                                    placeholder="Select category",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            [
                                html.Label("Product Name", className="filter-label"),
                                dbc.Input(id="add-product-name", type="text", placeholder="Product name"),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            [
                                html.Label("Product Price", className="filter-label"),
                                dbc.Input(
                                    id="add-product-price",
                                    type="number",
                                    placeholder="Price",
                                    min=0,
                                    step=0.01,
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            [
                                html.Label("Sales Date", className="filter-label"),
                                dcc.DatePickerSingle(
                                    id="add-sales-date",
                                    display_format="YYYY-MM-DD",
                                    className="date-picker-single",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                    ],
                    className="g-3",
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Country", className="filter-label"),
                                dcc.Dropdown(
                                    id="add-country",
                                    options=options_from_column("country"),
                                    placeholder="Select country",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            [
                                html.Label("City", className="filter-label"),
                                dbc.Input(id="add-city", type="text", placeholder="City"),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            [
                                html.Label("Sales Channel", className="filter-label"),
                                dcc.Dropdown(
                                    id="add-sales-channel",
                                    options=options_from_column(
                                        "sales_channel",
                                        fallback=[
                                            "Online",
                                            "Retail",
                                            "Partner",
                                            "Marketplace",
                                            "Direct",
                                        ],
                                    ),
                                    placeholder="Select channel",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                        dbc.Col(
                            [
                                html.Label("Order Status", className="filter-label"),
                                dcc.Dropdown(
                                    id="add-order-status",
                                    options=options_from_column(
                                        "order_status",
                                        fallback=[
                                            "Completed",
                                            "Pending",
                                            "Cancelled",
                                            "Returned",
                                        ],
                                    ),
                                    placeholder="Select status",
                                ),
                            ],
                            xs=12,
                            md=6,
                            lg=3,
                            className="mb-3",
                        ),
                    ],
                    className="g-3",
                ),

                dbc.Button(
                    "Add Record",
                    id="add-sale-button",
                    color="primary",
                    n_clicks=0,
                    className="mt-2",
                ),
            ]
        ),
        className="management-card mb-4",
    )


def build_management_table(df):
    """
    Editable table for updating and deleting sale records.
    """

    if df.empty:
        table_df = pd.DataFrame(columns=TABLE_COLUMNS)
    else:
        existing_columns = [col for col in TABLE_COLUMNS if col in df.columns]
        table_df = df[existing_columns].copy()

    return dash_table.DataTable(
        id="management-table",
        data=table_df.to_dict("records"),
        columns=[
            {
                "name": col.replace("_", " ").title(),
                "id": col,
                "editable": col != "id",
                "type": "numeric" if col == "product_price" else "text",
            }
            for col in table_df.columns
        ],
        editable=True,
        row_selectable="multi",
        selected_rows=[],
        page_size=12,
        sort_action="native",
        filter_action="native",
        fixed_rows={"headers": True},
        style_table={
            "overflowX": "auto",
            "overflowY": "auto",
            "maxHeight": "620px",
            "border": "1px solid #e5e7eb",
            "borderRadius": "14px",
        },
        style_header={
            "backgroundColor": "#0f172a",
            "color": "white",
            "fontWeight": "700",
            "border": "none",
            "fontSize": "13px",
            "textTransform": "uppercase",
            "letterSpacing": "0.04em",
        },
        style_cell={
            "fontFamily": "Inter, system-ui, sans-serif",
            "fontSize": "14px",
            "padding": "12px",
            "border": "1px solid #f1f5f9",
            "textAlign": "left",
            "minWidth": "120px",
            "maxWidth": "260px",
            "whiteSpace": "normal",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#f8fafc",
            },
            {
                "if": {"state": "selected"},
                "backgroundColor": "#dbeafe",
                "border": "1px solid #2563eb",
            },
        ],
    )


def build_data_management_tab(df):
    """
    Full Manage Data tab layout.
    """

    return html.Div(
        [
            build_add_sale_form(df),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H2("Edit Existing Sales", className="section-title"),
                        html.P(
                            "Edit records directly in the table, then click Save Edits. Select rows and click Delete Selected to remove them.",
                            className="section-subtitle",
                        ),

                        html.Div(
                            [
                                dbc.Button(
                                    "Save Edits",
                                    id="save-edits-button",
                                    color="success",
                                    n_clicks=0,
                                    className="me-2 mb-3",
                                ),
                                dbc.Button(
                                    "Delete Selected",
                                    id="delete-selected-button",
                                    color="danger",
                                    outline=True,
                                    n_clicks=0,
                                    className="mb-3",
                                ),
                            ],
                            className="management-actions",
                        ),

                        html.Div(
                            id="management-message",
                            className="management-message mb-3",
                        ),

                        html.Div(
                            id="management-table-container",
                            children=build_management_table(df),
                        ),
                    ]
                ),
                className="management-card mb-4",
            ),
        ]
    )
