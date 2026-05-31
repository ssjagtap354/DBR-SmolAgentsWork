from databricks.sdk import WorkspaceClient
import os
from dotenv import load_dotenv
import pandas as pd

# Load all Env's
load_dotenv()

# ✅ Check env variables loaded first
print("Hostname  :", os.environ.get("DATABRICKS_SERVER_HOSTNAME"))
print("HTTP Path :", os.environ.get("DATABRICKS_HTTP_PATH"))
print("Token     :", str(os.environ.get("DATABRICKS_TOKEN"))[:10], "...")

client = None

def try_connect_to_dbr():
    global client 
    client = WorkspaceClient(
            host=f"https://{os.environ.get('DATABRICKS_SERVER_HOSTNAME')}",
            token=os.environ.get("DATABRICKS_TOKEN")
        )
        
    # Test by listing clusters
    print("✅ Connected! Testing access...")
    warehouses = client.warehouses.list()
    for w in warehouses:
        print(f"   → Warehouse found: {w.name} | {w.state}")

def get_gold_data() -> pd.DataFrame:

    cursor = None  # ✅ define cursor outside try so finally can access it
    try:
        
        try_connect_to_dbr()
        
        # Create Cursor 
        response = client.statement_execution.execute_statement(
            warehouse_id=os.environ.get("DATABRICKS_SQL_WH_ID"),
            statement="Select * from ecommerce.gold.fact_orders limit 3"
        )

        # Create Pandas DF from the response Object. 
        
        # Get the column names 
        col_names = [each.name for each in response.manifest.schema.columns]
        # print(col_names)

        # Get all data for the columns 
        rows = response.result.data_array
        
        # Convert it to Pandas DF.

        df = pd.DataFrame(data=rows, columns=col_names)
        print("Dataframe generated. ")
        return df

        

    except Exception as e:
        print(f"❌ Error: {e}")

get_gold_data()