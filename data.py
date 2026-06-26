import pandas as pd
from supabase import create_client

from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_TABLE, DISPLAY_COLUMNS


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


import pandas as pd
from supabase import create_client

from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_TABLE, DISPLAY_COLUMNS


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_sales_data():
    """
    Pulls sales data from Supabase and returns a cleaned pandas DataFrame.
    """

    response = (
        supabase
        .table(SUPABASE_TABLE)
        .select("*")
        .range(0, 999)
        .execute()
    )

    data = response.data or []
    df = pd.DataFrame(data)

    if df.empty:
        return pd.DataFrame(columns=DISPLAY_COLUMNS)

    if "product_price" in df.columns:
        df["product_price"] = pd.to_numeric(df["product_price"], errors="coerce").fillna(0)

    if "sales_date" in df.columns:
        df["sales_date"] = pd.to_datetime(df["sales_date"], errors="coerce")
        df["sales_year"] = df["sales_date"].dt.year
        df["sales_month"] = df["sales_date"].dt.month_name()
        df["sales_month_number"] = df["sales_date"].dt.month
        df["sales_quarter"] = df["sales_date"].dt.to_period("Q").astype(str)

        # Convert back to string so Dash can safely store it in dcc.Store
        df["sales_date"] = df["sales_date"].dt.strftime("%Y-%m-%d")

    existing_columns = [col for col in DISPLAY_COLUMNS if col in df.columns]

    # Keep calculated date fields too, if they exist
    calculated_columns = [
        col for col in [
            "sales_year",
            "sales_month",
            "sales_month_number",
            "sales_quarter",
        ]
        if col in df.columns
    ]

    df = df[existing_columns + calculated_columns]

    return df


