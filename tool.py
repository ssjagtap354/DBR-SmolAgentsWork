from smolagents import tool
from get_gold_data import load_all_required_tables
import pandas as pd
import io

# Load required tables at module level (once, not on every tool call)
ALL_TABLE_DATA = load_all_required_tables()
df = ALL_TABLE_DATA['orders'].copy()

# Data type conversion — important for agent to get correct dtypes
df["dt"]                  = pd.to_datetime(df["dt"])
df["order_ts"]            = pd.to_datetime(df["order_ts"])
df["customer_id"]         = df["customer_id"].astype(str)
df["order_id"]            = df["order_id"].astype(int)
df["item_seq"]            = df["item_seq"].astype(int)
df["product_id"]          = df["product_id"].astype(int)
df["quantity"]            = df["quantity"].astype(int)
df["unit_price_currency"] = df["unit_price_currency"].astype(str)
df["unit_price"]          = df["unit_price"].astype(int)
df["discount_pct"]        = df["discount_pct"].astype(float)
df["tax_amount"]          = df["tax_amount"].astype(int)
df["channel"]             = df["channel"].astype(str)
df["coupon_code"]         = df["coupon_code"].astype(str)
df["gross_amt"]           = df["gross_amt"].astype(float)
df["discount_amt"]        = df["discount_amt"].astype(float)
df["sale_amt"]            = df["sale_amt"].astype(float)
df["coupon_flag"]         = df["coupon_flag"].astype(bool)
df["price_in_inr"]        = df["price_in_inr"].astype(float)


@tool
def query_fact_orders(question: str) -> str:
     
    
    """
    Retrieves orders data as a CSV string. 
    Load it into pandas using: df = pd.read_csv(io.StringIO(orders_data))

    Args:
        question: The question asked by the user about order data.
    """
    try:
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()
    except Exception as e:
        return f"Error accessing the Orders data: {str(e)}"
