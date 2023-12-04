from datasourcer import sourcing
from dataanalyzer import analyzer

from enum import Enum
from typing import Optional

from sqlmodel import create_engine, SQLModel, Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BASE_LOCATION = r"C:\Users\shrav\Downloads\uploads\\"

# origins allowed to send a request
origins = [
    "http://localhost",
    "http://localhost:8080",
]

class Filedata(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

# database initialization
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

app = FastAPI()
app.include_router(sourcing.router)
app.include_router(analyzer.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # includes authorization headers, cookies, etc
    allow_methods=["*"], # HTTP methods : POST, PUT or *
    allow_headers=["*"] # HTTP headers : Accept, Accept-Language, Content-Language, Content-Type or *
)

@app.get("/")
async def root():
    return {"message": "API to get Chat-GPT like features on your company data"}