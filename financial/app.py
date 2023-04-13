from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse, docs_url="/api/docs", openapi_url="/api/openapi.json")


@app.get("/api/financial_data")
def financial_data():
    return {"Hello": "financial_data"}


@app.get("/api/statistics")
def statistics():
    return {"Hello": "statistics"}
