from typing import List
from fastapi import FastAPI, Form, UploadFile, File
import pandas as pd
from PyPDF2 import PdfReader


app = FastAPI()


@app.post("/feedBack form/")
async def File(
    name: str = Form(...), phone_number: str = Form(...), Rating: int = Form(...)
):
    return f"Hi {name} successFully submited your Feedback !"


@app.post("/File/upload")  # FIle upload for single File
async def File_upload(file: UploadFile = File(...)):
    conetnt = await file.read()

    try:
        preview = conetnt.decode("utf-8")[:200]
    except e:
        preview = "can't able to preview the file"

    return {
        "File_name": file.filename,
        "Content_Type": file.content_type,
        "Size": len(conetnt),
        "Preview": preview,
    }


@app.post("/Multiple/File_Upload") # Multiple File Upload
async def Multiple_Fileupload(file: List[UploadFile] = File(...)):
    res = []

    for i in file:

        Content = await i.read()

        try:
            preview = Content.decode("utf-8")[:200]
        except e:
            preview = "can't able to preview the file"

        res.append(
            {
                "File_name": i.filename,
                "Content_Type": i.content_type,
                "Size": len(Content),
                "Preview": preview,
            }
        )
    return res


@app.post('/Any/File_Upload')
async def Any_file (file: List[UploadFile] = File(...)):
    pass