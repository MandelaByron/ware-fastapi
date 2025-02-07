import httpx
from typing import List, Dict, Optional, Tuple


async def add_items_to_cart(client: httpx.AsyncClient, items: List[Dict]) -> Dict:
    url = "https://connect.soligent.net/store/services/LiveOrder.Line.Service.ss"
    querystring = {"c": "3510556", "n": "2"}

    payload = [
        {
            "item": {"internalid": item["internalid"]},
            "quantity": item["quantity"],
            "location": "",
            "fulfillmentChoice": "ship",
            "freeGift": False
        }
        for item in items
    ]

    response = await client.post(url=url, json=payload, params=querystring, timeout=120)
    return response.json()


async def add_new_address(client: httpx.AsyncClient, payload: Dict) -> Tuple[Optional[int], Dict]:
    url = "https://connect.soligent.net/store/services/Address.Service.ss"
    querystring = {"c": "3510556", "n": "2"}

    response = await client.post(url, json=payload, params=querystring, timeout=120)
    data = response.json()
    
    return data.get("internalid"), data


async def get_item_data(sku: str, client: httpx.AsyncClient) -> Optional[int]:
    url = "https://connect.soligent.net/api/personalized/items"
    querystring = {
        "language": "en", "currency": "USD", "c": "3510556", "offset": "0",
        "sitepath": "/store/searchApi.ssp", "sort": "relevance:desc",
        "use_pcv": "F", "fieldset": "search", "n": "2", "q": sku,
        "include": "", "limit": "1", "country": "US", "pricelevel": "4"
    }

    response = await client.get(url, params=querystring)
    data = response.json()

    if data.get("items"):
        item = data["items"][0]
        return item["internalid"] if sku == item["itemid"] else None

    return None

async def check_login(client: httpx.AsyncClient) -> bool:
    
    url = "https://connect.soligent.net/store/services/ShoppingUserEnvironment.Service.ss"   
    querystring = {"lang":"en_US","cur":"","X-SC-Touchpoint":"shopping"}
    response = await client.get(url, params=querystring)
    
    response_data = response.json()
    
    status = response_data['ENVIRONMENT']['PROFILE']['isLoggedIn']
    
    if status == "F":
        return False
    elif status == "T":
        return True







# response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

# print(response.text)