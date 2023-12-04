import main

from enum import Enum

from sqlmodel import Session, select
from fastapi import APIRouter, File, UploadFile

router = APIRouter()

class FileType(str, Enum):
    excel = "xlsx"
    csv = "csv"
    txt = "txt"

# Send the file @ http://localhost:8000/datasourcer/file_upload?file_type=xlsx
@router.post("/datasourcer/file_upload")
async def read_item(file_type : FileType, file: UploadFile = File(...)):
    try:
        with open(main.BASE_LOCATION + file.filename, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
        
        new_file = main.Filedata(name= file.filename)
        
        with Session(main.engine) as session:
            session.add(new_file)
            print("Database updated")
            print(session.commit())
            statement = select(main.Filedata.id).order_by(main.Filedata.id.desc())
            count = session.exec(statement).first()

    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"message": f"Successfully uploaded {file.filename} and generated the ID {count}"}