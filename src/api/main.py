from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.webhooks import router as webhooks_router

app = FastAPI(
    title="OrionSync API",
    description="Zero-UI Operations Orchestrator for the Deskless Economy",
    version="1.0.0"
)

# Standard middleware to prevent local testing CORS headaches
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A lightweight health check. Crucial for verifying deployments 
# before walking on stage for the live demo.
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "operational", "system": "OrionSync"}

# Mount the webhook endpoints
app.include_router(webhooks_router, prefix="/api/v1/webhooks", tags=["Webhooks"])