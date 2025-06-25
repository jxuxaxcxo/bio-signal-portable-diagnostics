import httpx

async def forward_request(service_url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(service_url, json=payload)
            response.raise_for_status()  # Raise exception for non-2xx status
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"Bad response from service: {e.response.status_code}", "detail": e.response.text}
        except Exception as e:
            return {"error": str(e)}
