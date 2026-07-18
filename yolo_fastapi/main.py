from pathlib import Path
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image, UnidentifiedImageError
from ultralytics import YOLO


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "yolo11n.pt"
UPLOAD_DIR = BASE_DIR / "uploads"
RESULT_DIR = BASE_DIR / "results"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
MAX_UPLOAD_SIZE = 10 * 1024 * 1024

UPLOAD_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)

app = FastAPI(title="YOLO11 Object Detection")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/results", StaticFiles(directory=str(RESULT_DIR)), name="results")

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))


def render_index(request: Request, **context):
    return templates.TemplateResponse("index.html", {"request": request, **context})


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return render_index(request)


@app.post("/detect", response_class=HTMLResponse)
async def detect(request: Request, file: UploadFile = File(...)):
    original_name = Path(file.filename or "").name
    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return render_index(request, error="请上传 jpg、jpeg、png、bmp 或 webp 格式的图片。")

    content = await file.read()
    if not content:
        return render_index(request, error="上传的文件为空，请重新选择图片。")

    if len(content) > MAX_UPLOAD_SIZE:
        return render_index(request, error="图片不能超过 10MB。")

    image_id = uuid4().hex
    input_path = UPLOAD_DIR / f"{image_id}{extension}"
    output_path = RESULT_DIR / f"{image_id}.jpg"

    input_path.write_bytes(content)

    try:
        with Image.open(input_path) as img:
            img.verify()
    except (UnidentifiedImageError, OSError):
        input_path.unlink(missing_ok=True)
        return render_index(request, error="文件内容不是有效图片，请重新上传。")

    try:
        started_at = perf_counter()
        results = model(str(input_path))
        elapsed_ms = round((perf_counter() - started_at) * 1000)
        results[0].save(filename=str(output_path))
    except Exception as exc:
        input_path.unlink(missing_ok=True)
        return render_index(request, error=f"检测失败：{exc}")

    detections = []
    names = results[0].names
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        detections.append(
            {
                "label": names.get(class_id, str(class_id)),
                "confidence": round(confidence * 100, 2),
            }
        )

    return render_index(
        request,
        result_image=f"results/{output_path.name}",
        detections=detections,
        detection_count=len(detections),
        elapsed_ms=elapsed_ms,
        original_name=original_name,
    )
