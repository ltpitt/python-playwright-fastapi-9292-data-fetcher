from fastapi import APIRouter, Query
from app.services import TravelService

router = APIRouter()

@router.get("/travel-data")
async def get_travel_data(
    start: str = Query(..., description="Starting point"),
    start_id: str = Query(..., description="Starting point ID"),
    destination: str = Query(..., description="Destination"),
    destination_id: str = Query(..., description="Destination ID")
):
    travel_service = TravelService()
    travel_data = await travel_service.fetch_travel_data(start, start_id, destination, destination_id)
    return travel_data
