import main

import os

from sqlmodel import Field, Session, SQLModel, select
from pandas import read_excel, read_csv
from fastapi import APIRouter
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

router = APIRouter()

@router.get("/dataanalyzer/analyze")
async def analyze_file(id: int, question: str):
    # get the file name from database
    with Session(main.engine) as session:
        statement = select(main.Filedata.name).where(main.Filedata.id == id)
        file_name = session.exec(statement).first()

    # get the file as a dataframe
    _, file_extension = os.path.splitext(file_name)
    if file_extension == ".xlsx":
        df = read_excel(main.BASE_LOCATION + file_name)
    elif file_extension == ".csv" or file_extension == ".txt":
        df = read_csv(main.BASE_LOCATION + file_name)
    else:
        return "File format not supported by the API. Try selecting a .xlsx, .csv or .txt"

    # load as a smartdataframe
    llm = OpenAI(api_token="YOUR TOKEN")
    sdf = SmartDataframe(df, config={"llm": llm})

    # return the output
    #df.chat('Which are the countries with GDP greater than 3000000000000?')
    return f"Got you covered : {question}"