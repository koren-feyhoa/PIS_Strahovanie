# storage.py
import uuid
import pathlib
import aiofiles
from fastapi import UploadFile


class FileStorage:
    @staticmethod
    async def save(upload_file: UploadFile, client_id:int) -> tuple[str,str]:
        """
        Сохраняет загруженный файл в указанную директорию.
        Генерирует уникальное имя, сохраняя расширение исходного файла.
        Возвращает путь к сохранённому файлу.
        """
        # Безопасно получаем расширение
        original_name = pathlib.Path(upload_file.filename)
        ext = original_name.suffix
        new_name = f"{uuid.uuid4().hex}{ext}"
        destination = pathlib.Path("files") / str(client_id) / new_name

        destination.parent.mkdir(parents=True, exist_ok=True)

        # Асинхронно записываем содержимое
        async with aiofiles.open(destination, "wb") as out_file:
            while chunk := await upload_file.read(1024 * 1024):
                await out_file.write(chunk)

        return str(destination.parent), str(destination.name)