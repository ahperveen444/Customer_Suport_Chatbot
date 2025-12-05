from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_API_KEY
import json

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def get_order(order_id):
    if order_id == 0:
        return {"orderID": "Please provide your Order Id to know details"}

    response = (
        supabase.table("orders")
        .select("*")
        .eq("id", order_id)
        .single()
        .execute()
    )
    
    data = response.data
    if data is None:
        return {"orderID": f"No order found for this Order ID : {order_id}"}
    
    return {"orderID": json.dumps(data)}
