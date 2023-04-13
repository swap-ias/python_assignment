from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from financial.api_financial import financial_router

app = FastAPI(default_response_class=ORJSONResponse, docs_url="/api/docs", openapi_url="/api/openapi.json")

app.include_router(financial_router, prefix="/api")
