from fastapi import FastAPI, Request, Depends
from app.shopify import get_order_properties
from app.solignet.cart import get_item_data ,add_new_address, add_items_to_cart
from app.deps import get_http_client
from app.gql import change_status
import re
import httpx
import asyncio
import json
import os
app = FastAPI()


api_version = os.environ.get('API_VERSION')

test_key = os.environ.get('TEST_KEY')

#client = client_manager.get_client()
@app.get("/")
def health_check():
    return {"status": "ok, this is my health check 3", 'API_VERSION': api_version, "TEST_KEY": test_key}

def format_us_phone(number: str) -> str:
    """Formats a U.S. phone number to (XXX) YYY-ZZZZ, handling +1 country code if present."""
    # Remove any non-digit characters
    digits = re.sub(r"\D", "", number)

    # Remove leading '1' if it's a U.S. country code
    if digits.startswith("1") and len(digits) == 11:
        digits = digits[1:]  # Remove the leading '1'

    # Ensure it's exactly 10 digits after processing
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    else:
        raise ValueError("Invalid phone number. Must contain 10 digits after processing.")

@app.post("/webhook")
async def webhook(request : Request, client: httpx.AsyncClient = Depends(get_http_client)):
    data = await request.json()
    
    eventData = data.get("event")
    
    pulseID = eventData["pulseId"]
    
    boardID = eventData['boardId']
    
    pulseName = eventData['pulseName']
    
    
    order_response = await get_order_properties(pulseName)
    
    order_data = order_response.get('data').get('order')
    
    shipping_data = order_data.get('shippingAddress')
    
    if shipping_data == None:
        shipping_data = order_data.get('billingAddress')
    
    fullname = shipping_data.get('name')
    
    company = shipping_data.get('company')
    
    phone_number = shipping_data.get('phone')
    
    
    if not company:
        company = fullname
        
    payload = {
        "country": shipping_data.get('countryCodeV2'),
        'fullname':fullname,
        'company': company,
        'addr1': shipping_data.get('address1'),
        'addr2': shipping_data.get('address2'),
        'city':shipping_data.get('city'),
        'state': shipping_data.get('provinceCode'),
        'phone':format_us_phone(phone_number) if phone_number else None,
        'zip':shipping_data.get('zip'),
        "isresidential": "T",
        "defaultshipping": "T",
    }

    # processed_items = []
    # items = [
    #     {"sku": item['sku'], "name": item['name'], 'quantity': item['quantity']}
    #     for item in order_data['lineItems']['nodes']
    # ]
        
    # for item in items:
    #     internalid = await get_item_data(sku=item['sku'], client=client)
    #     if internalid:
    #         item['internalid'] = internalid
    #         processed_items.append(item)  # Keep only valid items
    #     # Execute independent API calls in parallel
    # await asyncio.gather(
    #     add_items_to_cart(client, items=processed_items),
    #     add_new_address(client=client, payload=payload),
    #     change_status(itemID=pulseID, board_id=boardID)
    # )


    # return data


