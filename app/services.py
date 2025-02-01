from app.utils.playwright_helper import PlaywrightHelper

class TravelService:
    async def fetch_travel_data(self, start: str, start_id: str, destination: str, destination_id: str):
        playwright_helper = PlaywrightHelper()
        travel_data = await playwright_helper.fetch_travel_data(start, start_id, destination, destination_id)
        return travel_data
