import argparse
import os
import json
from ultralytics import YOLO

def main():
    try:
        parser = argparse.ArgumentParser(description='Загрузка файла и обработка нейросетью')
        parser.add_argument('input_file', help='Путь к файлу изображения или видео')
        parser.add_argument('-t', '--type', choices=['image', 'video'], default='image',
                            help='Тип файла (image - изображение, video - видео)')
        args = parser.parse_args()

        input_file = args.input_file
        file_type = args.type
    except Exception as e:
        print(f"Неверный формат/не загружен: {e}")
        return None

    # проверка существования файла
    if not os.path.isfile(input_file):
        print(f'Файл не найден: {input_file}')
        exit(1)

    # обработка файла
    model = YOLO("/Users/sexyboy/Desktop/Hackathon/bpla/bpla/best.pt")

    if file_type == "image":
        res = model(input_file, save=True)
        json_data = []
        for result in res:
            filename = os.path.basename(input_file)
            objects = []
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]  # Get the bounding box coordinates
                width = x2 - x1
                height = y2 - y1
                obj_class = box.cls.item()  # Get the object class
                obj_data = {
                    "obj_class": str(obj_class),
                    "x": str(x1.item()),
                    "y": str(y1.item()),
                    "width": str(width.item()),
                    "height": str(height.item())
                }
                objects.append(obj_data)
            frame_data = {
                "filename": filename,
                "objects": objects
            }
            json_data.append(frame_data)

        # Save JSON data to file
        json_file_path = os.path.splitext(input_file)[0] + "_detections.json"
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f'Detections saved to {json_file_path}')

if __name__ == '__main__':
    main()