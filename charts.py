import pandas as pd
import plotly.express as px

import plotly.graph_objects as go


def make_sales_map(df):
    """
    Creates a world map showing number of sales by country.
    """

    if df.empty or "country" not in df.columns:
        return px.choropleth(title="Sales by Country")

    country_sales = (
        df.groupby("country", dropna=False)
        .size()
        .reset_index(name="sales_count")
        .sort_values("sales_count", ascending=False)
    )

    fig = px.choropleth(
        country_sales,
        locations="country",
        locationmode="country names",
        color="sales_count",
        hover_name="country",
        hover_data={"sales_count": True, "country": False},
        color_continuous_scale="Blues",
        title="Number of Sales by Country",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=55, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, system-ui, sans-serif",
            color="#111827",
        ),
        title=dict(
            font=dict(size=20, color="#0f172a"),
            x=0.02,
            xanchor="left",
        ),
        coloraxis_colorbar=dict(
            title="Sales",
            thickness=14,
            len=0.75,
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#cbd5e1",
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)",
        ),
    )

    return fig


def make_sales_by_category_chart(df):
    """
    Creates a horizontal bar chart showing total sales value by product category.
    If product_price is unavailable, it falls back to count of rows.
    """

    if df.empty or "product_cat" not in df.columns:
        return px.bar(title="Sales by Product Category")

    if "product_price" in df.columns:
        category_sales = (
            df.groupby("product_cat", dropna=False)["product_price"]
            .sum()
            .reset_index(name="total_sales")
            .sort_values("total_sales", ascending=True)
        )

        category_sales = category_sales.tail(10)


        fig = px.bar(
            category_sales,
            x="total_sales",
            y="product_cat",
            orientation="h",
            text="total_sales",
            title="Top 10 Product Categories by Sales Value",
            labels={
                "product_cat": "Product Category",
                "total_sales": "Total Sales Value",
            },
            color="total_sales",
            color_continuous_scale=[
                [0.0, "#93c5fd"],
                [0.5, "#3b82f6"],
                [1.0, "#1e3a8a"],
            ],
        )



        fig.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside",
            marker_line_width=0,
        )

        fig.update_xaxes(tickprefix="$", separatethousands=True)

    else:
        category_sales = (
            df.groupby("product_cat", dropna=False)
            .size()
            .reset_index(name="sales_count")
            .sort_values("sales_count", ascending=True)
        )

        fig = px.bar(
            category_sales,
            x="sales_count",
            y="product_cat",
            orientation="h",
            text="sales_count",
            title="Number of Sales by Product Category",
            labels={
                "product_cat": "Product Category",
                "sales_count": "Number of Sales",
            },
            color="sales_count",
            color_continuous_scale="Blues",
        )

        fig.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            marker_line_width=0,
        )

    fig.update_layout(
        margin=dict(l=10, r=35, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, system-ui, sans-serif",
            color="#111827",
        ),
        title=dict(
            font=dict(size=20, color="#0f172a"),
            x=0.02,
            xanchor="left",
        ),
        xaxis=dict(
            title=None,
            gridcolor="#e5e7eb",
        ),
        yaxis=dict(
            title=None,
            automargin=True,
        ),
        coloraxis_showscale=False,
        bargap=0.35,
    )

    return fig

def make_empty_figure(title):
    fig = go.Figure()

    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, system-ui, sans-serif",
            color="#111827",
        ),
        annotations=[
            dict(
                text="No data available for the selected filters",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=15, color="#64748b"),
            )
        ],
    )

    return fig


def apply_common_layout(fig, title):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color="#0f172a"),
            x=0.02,
            xanchor="left",
        ),
        margin=dict(l=10, r=25, t=60, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, system-ui, sans-serif",
            color="#111827",
        ),
        xaxis=dict(
            gridcolor="#e5e7eb",
        ),
        yaxis=dict(
            gridcolor="#e5e7eb",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    return fig


def make_sales_trend_chart(df):
    """
    Monthly revenue trend based on sales_date and product_price.
    """

    title = "Revenue Trend Over Time"

    if df.empty or "sales_date" not in df.columns or "product_price" not in df.columns:
        return make_empty_figure(title)

    trend_df = df.copy()
    trend_df["sales_date"] = pd.to_datetime(trend_df["sales_date"], errors="coerce")
    trend_df["product_price"] = pd.to_numeric(trend_df["product_price"], errors="coerce").fillna(0)

    trend_df = trend_df.dropna(subset=["sales_date"])

    if trend_df.empty:
        return make_empty_figure(title)

    monthly_sales = (
        trend_df
        .set_index("sales_date")
        .resample("ME")
        .agg(
            revenue=("product_price", "sum"),
            orders=("id", "count"),
        )
        .reset_index()
    )

    fig = px.line(
        monthly_sales,
        x="sales_date",
        y="revenue",
        markers=True,
        title=title,
        labels={
            "sales_date": "Month",
            "revenue": "Revenue",
        },
    )

    fig.update_traces(
        line=dict(color="#2563eb", width=3),
        marker=dict(size=8, color="#1d4ed8"),
        hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
    )

    fig.update_yaxes(tickprefix="$", separatethousands=True)

    return apply_common_layout(fig, title)


def make_revenue_by_channel_chart(df):
    """
    Revenue by sales channel.
    """

    title = "Revenue by Sales Channel"

    if df.empty or "sales_channel" not in df.columns or "product_price" not in df.columns:
        return make_empty_figure(title)

    channel_sales = (
        df.groupby("sales_channel", dropna=False)["product_price"]
        .sum()
        .reset_index(name="revenue")
        .sort_values("revenue", ascending=True)
    )

    fig = px.bar(
        channel_sales,
        x="revenue",
        y="sales_channel",
        orientation="h",
        text="revenue",
        title=title,
        labels={
            "sales_channel": "Sales Channel",
            "revenue": "Revenue",
        },
    )

    fig.update_traces(
        marker_color="#0ea5e9",
        marker_line_color="#0369a1",
        marker_line_width=1,
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>",
    )

    fig.update_xaxes(tickprefix="$", separatethousands=True)
    fig.update_yaxes(automargin=True)

    return apply_common_layout(fig, title)


def make_order_status_chart(df):
    """
    Donut chart showing order status breakdown.
    """

    title = "Order Status Breakdown"

    if df.empty or "order_status" not in df.columns:
        return make_empty_figure(title)

    status_counts = (
        df.groupby("order_status", dropna=False)
        .size()
        .reset_index(name="orders")
        .sort_values("orders", ascending=False)
    )

    fig = px.pie(
        status_counts,
        names="order_status",
        values="orders",
        hole=0.55,
        title=title,
        color_discrete_sequence=[
            "#2563eb",
            "#0ea5e9",
            "#22c55e",
            "#f97316",
            "#ef4444",
            "#64748b",
        ],
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>",
    )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color="#0f172a"),
            x=0.02,
            xanchor="left",
        ),
        margin=dict(l=10, r=10, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, system-ui, sans-serif",
            color="#111827",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig


def make_top_products_chart(df):
    """
    Top 10 products by revenue.
    """

    title = "Top 10 Products by Revenue"

    if df.empty or "product_name" not in df.columns or "product_price" not in df.columns:
        return make_empty_figure(title)

    product_sales = (
        df.groupby("product_name", dropna=False)["product_price"]
        .sum()
        .reset_index(name="revenue")
        .sort_values("revenue", ascending=False)
        .head(10)
        .sort_values("revenue", ascending=True)
    )

    fig = px.bar(
        product_sales,
        x="revenue",
        y="product_name",
        orientation="h",
        text="revenue",
        title=title,
        labels={
            "product_name": "Product",
            "revenue": "Revenue",
        },
    )

    fig.update_traces(
        marker_color="#2563eb",
        marker_line_color="#1e40af",
        marker_line_width=1,
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>",
    )

    fig.update_xaxes(tickprefix="$", separatethousands=True)
    fig.update_yaxes(automargin=True)

    return apply_common_layout(fig, title)
