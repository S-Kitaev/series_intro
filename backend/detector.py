import cv2
from ultralytics import YOLO

FRAME_STEP    = 8
TARGET_SIZE   = (224, 224)
PROB_THRESHOLD = 0.5

# подгружаем модель нейросети
_model = YOLO("backend/models/model.pt")

# функция определения начала и конца заставки в видео
def detect_intro(video_path: str):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    idx = 0
    preds = []

    # Предсказываем вероятность каждого 8го кадра быть заставкой
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % FRAME_STEP == 0:
            img = cv2.resize(frame, TARGET_SIZE)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            res = _model.predict(img, verbose=False)
            prob = res[0].probs.data[1].item()
            preds.append(1 if prob > PROB_THRESHOLD else 0)
        idx += 1

    cap.release()

    # сглаживаем результат, чтобы избавиться от TN и FP
    n = len(preds)
    sm = [0]*n
    for i in range(n):
        if sum(preds[max(0,i-9):i+1]) >= 7 or sum(preds[i:min(n,i+10)]) >= 7:
            sm[i] = 1

    if 1 not in sm:
        return None, None

    first = sm.index(1)
    last  = n-1 - sm[::-1].index(1)
    sf = first * FRAME_STEP
    lf = last  * FRAME_STEP

    def fmt(sec):
        h = int(sec//3600)
        m = int((sec%3600)//60)
        s = int(sec%60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    return fmt(sf/fps), fmt(lf/fps)