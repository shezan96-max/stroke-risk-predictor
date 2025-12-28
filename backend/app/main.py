from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schemas import StrokeInput
from app.service import predict

app = FastAPI(title="Stroke Risk Detector",version=1.0)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("frontend/index.html")


@app.get("/")
def root():
    return {"message": "Stroke Risk Prediction API is running"}

@app.post("/predict")
def predict_stroke(input_data: StrokeInput, explain: bool = False):
    result = predict(input_data, explain=explain)

    # 🔥 DO NOT FILTER RESPONSE
    return result
