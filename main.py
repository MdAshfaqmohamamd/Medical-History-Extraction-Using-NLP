from fastapi import FastAPI, Form, UploadFile, File, HTTPException
import uvicorn
from extractor import extract
import uuid
import os
import logging

from db_utils import init_db
init_db()

# Setting up logger
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

app = FastAPI()

@app.post("/extract_from_doc")
async def extract_from_doc(
    file: UploadFile = File(...),
    file_format: str = Form(...)
):
    try:
        logger.info("Starting file upload and extraction process.")
        content = await file.read()

        FILE_PATH = os.path.join(
            r"C:\Users\Admin\Desktop\projects\medical data extraction\backend\uploads",
            str(uuid.uuid4()) + ".pdf"
        )

        with open(FILE_PATH, "wb") as f:
            f.write(content)
        logger.info(f"File saved at {FILE_PATH}")

        data = extract(FILE_PATH, file_format)
        logger.info(f"Extraction completed for file format: {file_format}")

        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)
            logger.info(f"Temporary file {FILE_PATH} removed.")

        return data

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

