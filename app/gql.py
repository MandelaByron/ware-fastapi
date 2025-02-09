import httpx
import json
import os

MONDAY_AUTH = os.environ.get("MONDAY_ACCESS_KEY")
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization' : MONDAY_AUTH
}
async def get_product_data(itemId):
    
    query = f"""
        query {{
        items (ids: [{itemId}]) {{
            id,
            name,
            column_values{{
            column{{
                title
            }}
            value
            }}
        }}
        }}
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url="https://api.monday.com/v2", headers=HEADERS, json={"query": query})
        
        data = response.json()
        with open('tabledata.json', 'w') as file:
            json.dump(data, file, indent=2)
        return data
 

async def change_status(itemID: int, board_id: int):
    """Change the status of an item on a Monday.com board."""
    
    mutation = """
        mutation ChangeStatus($board_id: ID!, $item_id: ID!, $value: String!) {
            change_simple_column_value (
                board_id: $board_id,
                item_id: $item_id,
                column_id: "status",
                value: $value
            ) {
                id
            }
        }
    """

    variables = {
        "board_id": board_id,
        "item_id": itemID,
        "value": "Done"  # Value must be a JSON string
    }

    url = "https://api.monday.com/v2"


    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={"query": mutation, "variables": variables},
            headers=HEADERS
        )

    return response.json()
