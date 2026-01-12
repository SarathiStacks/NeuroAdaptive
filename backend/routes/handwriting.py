from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import requests
import cv2
import numpy as np
from tensorflow import keras
from dotenv import load_dotenv

load_dotenv()
VISION_KEY = os.getenv("AZURE_VISION_KEY")
VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
MODEL_PATH = r"D:\Micro Imagine cup\NeuroAdaptive\backend\models\dyslexia_handwriting_cnn.h5"
HW_MODEL = keras.models.load_model(
    MODEL_PATH,
    compile=False
)
router = APIRouter(prefix="/handwriting", tags=["Handwriting"])
def call_azure_ocr(image_bytes: bytes):
    url = f"{VISION_ENDPOINT}/vision/v3.2/ocr"
    headers = {
        "Ocp-Apim-Subscription-Key": VISION_KEY,
        "Content-Type": "application/octet-stream",
    }

    response = requests.post(url, headers=headers, data=image_bytes)

    if response.status_code != 200:
        raise RuntimeError(
            f"Azure OCR request failed: {response.status_code} {response.text}"
        )

    ocr_json = response.json()

    extracted_text = []
    for region in ocr_json.get("regions", []):
        for line in region.get("lines", []):
            words = [w["text"] for w in line.get("words", [])]
            extracted_text.append(" ".join(words))

    return "\n".join(extracted_text)

def get_clarity_score(image_bytes: bytes) -> float:
    img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ValueError("Invalid image")

    # Handle grayscale
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # Handle alpha channel
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # BGR → RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize to training size
    img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_AREA)
    
    img = img.astype(np.float32) / 255.0

    img = np.expand_dims(img, axis=0)

    prediction = HW_MODEL.predict(img, verbose=0)[0][0]
    return float(prediction)

print("Model input shape:", HW_MODEL.input_shape)
print("Model output shape:", HW_MODEL.output_shape)
HW_MODEL.summary()


@router.post("/upload")
async def handwriting_upload(file: UploadFile = File(...)):
    image_bytes = await file.read()

    try:
        extracted = call_azure_ocr(image_bytes)
        clarity = get_clarity_score(image_bytes)

        return JSONResponse({
            "extractedText": extracted,
            "clarityScore": clarity,
            "message": "You're doing great! Try clearer lighting if needed.",
            "improvement": None if clarity > 0.75 else ["Try improving clarity slightly!"]
        })

    except Exception as e:
        print("Handwriting error:", e)
        return JSONResponse({"error": str(e)}, status_code=500)
