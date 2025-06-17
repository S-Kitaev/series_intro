import cv2
import torch

# Константы
FRAME_STEP = 8
TARGET_SIZE = (224, 224)

class IntroDetector:
    def __init__(self, model_path: str, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        # Загрузка модели
        self.model = torch.load(model_path, map_location=self.device)
        self.model.eval()

    def detect(self, video_path: str):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open video {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_idx = 0
        preds = []

        # Проходим по кадрам
        with torch.no_grad():
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                # берем каждый 8-й кадр
                if frame_idx % FRAME_STEP != 0:
                    frame_idx += 1
                    continue

                # Предобработка кадра
                img = cv2.resize(frame, TARGET_SIZE, interpolation=cv2.INTER_AREA)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).float() / 255.0
                tensor = tensor.to(self.device)

                # Предсказание
                out = self.model(tensor)
                prob = torch.softmax(out, dim=1)[0, 1].item()
                preds.append(1 if prob > 0.5 else 0)
                frame_idx += 1
        cap.release()

        # Сглаживание: считаем кадр 1, если в окне из 10 предсказаний слева или справа >=7 единиц
        n = len(preds)
        smoothed = [0] * n
        for i in range(n):
            left_start = max(0, i - 9)
            right_end = min(n, i + 10)
            if sum(preds[left_start:i+1]) >= 7 or sum(preds[i:right_end]) >= 7:
                smoothed[i] = 1


        if 1 not in smoothed:
            return None, None

        # Индексы первого и последнего 1
        first = smoothed.index(1)
        last = n - 1 - smoothed[::-1].index(1)

        # Перевод в кадров в секунды
        start_frame = first * FRAME_STEP
        end_frame = last * FRAME_STEP
        t0 = start_frame / fps
        t1 = end_frame / fps

        # Форматирование
        def fmt(sec):
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s = int(sec % 60)
            return f"{h:02d}:{m:02d}:{s:02d}"

        return fmt(t0), fmt(t1)