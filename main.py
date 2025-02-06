from ftp_service import FTPService
from utils import remove_duplicates

import os
from fastapi import FastAPI, HTTPException, Query
import pandas as pd


app = FastAPI()

FTP_CONFIG = {
    "host": os.getenv("FTP_HOST"),
    "port": int(os.getenv("FTP_PORT")),
    "username": os.getenv("FTP_USERNAME"),
    "password": os.getenv("FTP_PASSWORD"),
}

ftp_service = FTPService(**FTP_CONFIG)


@app.get("/file/list")
def list_files():
    DIRECTORY = "/SIAPE"
    try:
        files = ftp_service.list_files_in_directory(DIRECTORY)
        return {"success": True, "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/file/read")
def read_file(target_file: str = Query(..., description="The name of the target file to read")):
    DIRECTORY = "/SIAPE"
    file_path = f"{DIRECTORY}/{target_file}"
    
    try:
        file_content = ftp_service.download_file(file_path)
        
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_content)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        df = df.dropna(axis=1, how='all')
        data = df.to_dict(orient='records')
        
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/file/column")
def get_column(
    target_file: str = Query(..., description="The name of the file to read"),
    target_column: str = Query(..., description="The name of the column to retrieve")
):
    DIRECTORY = "/SIAPE"
    file_path = f"{DIRECTORY}/{target_file}"
    
    try:
        file_content = ftp_service.download_file(file_path)
        
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_content)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        if target_column not in df.columns:
            raise HTTPException(status_code=404, detail=f"Column '{target_column}' not found")
        
        column_data = df[target_column].dropna().tolist()
        no_duplicates_column_data = remove_duplicates(column_data)
        
        return {"success": True, "column_data": no_duplicates_column_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
