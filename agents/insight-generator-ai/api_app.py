from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import zipfile
from parser import load_data
from visualizer import generate_charts

app = FastAPI()

# CORS for master frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "✅ Insight Generator AI backend is running!"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    filepath = f"sample_data/{file.filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = load_data(filepath)
    chart_info = generate_charts(df)

    return JSONResponse(content={"charts": chart_info})

@app.get("/download_zip")
def download_zip():
    zip_filename = "charts.zip"
    zip_path = f"./{zip_filename}"

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir("outputs"):
            if file.endswith(".png"):
                zipf.write(os.path.join("outputs", file), arcname=file)

    return FileResponse(zip_path, filename=zip_filename, media_type='application/zip')
