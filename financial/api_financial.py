from fastapi import APIRouter

financial_router = APIRouter()


@financial_router.get("/financial_data")
def financial_data():
    return {"Hello": "financial_data"}


@financial_router.get("/statistics")
def statistics():
    return {"Hello": "statistics"}
