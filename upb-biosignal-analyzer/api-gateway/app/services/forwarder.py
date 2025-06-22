import httpx

async def forward_request(service_url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(service_url, json=payload)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
