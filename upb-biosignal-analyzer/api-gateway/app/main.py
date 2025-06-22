from fastapi import FastAPI
from app.routes import router_analysis

app = FastAPI(title="API Gateway")

app.include_router(router_analysis.router, prefix="/analyze")