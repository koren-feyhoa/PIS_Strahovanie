import pathlib
import uuid

import models
from sqlalchemy.orm import Session
import aiofiles
from fastapi import FastAPI, UploadFile, File
async def saveFile(upload_file: UploadFile, path: pathlib.Path):
    original_name= pathlib.Path(UploadFile.filename)
    new_name=str(uuid.uuid4())
    destination=path/new_name
    destination.parent.mkdir(parents=True,exist_ok=True)
    async with aiofiles.open(path, "wb") as out_file:
        while content := await upload_file.read(1024 * 1024):  # читаем по 1 МБ
            await out_file.write(content)
    return destination



