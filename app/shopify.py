import httpx
import json
import os
import asyncio



SHOP_URL = os.environ.get("SHOPIFY_URL")
API_VERSION = os.environ.get("API_VERSION")
TOKEN = os.environ.get("SHOPIFY_ACCESS_TOKEN")
# Shopify GraphQL URL and Headers
GRAPHQL_URL = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": TOKEN,   
    "Content-Type": "application/json"
}

async def get_order_properties(orderID: str) -> dict:

    query = """
        query ($id: ID!){
        order(id: $id) {
            id
            name
            shippingAddress{
                address1
                address2
                city
                company
                countryCodeV2
                zip
                provinceCode
                phone
                name                
            }
            billingAddress{
                address1
                address2
                city
                company
                countryCodeV2
                zip
                provinceCode
                phone
                name                
            }            
            totalPriceSet {
            presentmentMoney {
                amount
            }
            }
            lineItems(first: 10) {
            nodes {
                id
                name
                sku
                quantity
            }
            }
        }
        }
    """
    
    variables = {
        "id":  f"gid://shopify/Order/{orderID}" 
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GRAPHQL_URL,headers=HEADERS, json={"query":query, "variables": variables})
        
        data = response.json()
        
        return data


