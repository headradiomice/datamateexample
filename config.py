import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "sales")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Missing SUPABASE_URL or SUPABASE_KEY. Check your .env file."
    )

TABLE_COLUMNS = [
    "id",
    "sales_date",
    "first_name",
    "last_name",
    "email",
    "gender",
    "product_cat",
    "product_name",
    "product_price",
    "country",
    "city",
    "sales_channel",
    "order_status",
]

DISPLAY_COLUMNS = TABLE_COLUMNS