from fastapi import APIRouter

router = APIRouter(prefix="/audio", tags=["Audio"])

# This route is no longer needed in ECG container under the new architecture.
# Communication with the audio service should occur via API Gateway.