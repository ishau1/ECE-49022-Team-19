from ultralytics import YOLO
import yaml

def create_data_yaml(class_path, data_path):
    with open(class_path, 'r') as file:
        classes = []
        for line in file.readlines():
            if len(line.strip()) == 0:
                continue
            classes.append(line.strip())
    num_classes = len(classes)

    data = {
        'path': '/Users/inmka/PycharmProjects/ObjectDetection49022/data',
        'train': '/Users/inmka/PycharmProjects/ObjectDetection49022/data/train/images',
        'val': '/Users/inmka/PycharmProjects/ObjectDetection49022/data/validation',
        'nc': num_classes,
        'names': classes
    }

    #writes data to YAML file
    with open(data_path, 'w') as file:
        yaml.dump(data, file, sort_keys=False)
    print(f'Created config file at {data_path}')

    return

#define path for classes.txt and data.yaml
class_path = '/Users/inmka/PycharmProjects/ObjectDetection49022/data/classes.txt'
data_path = '/Users/inmka/PycharmProjects/ObjectDetection49022/data.yaml'

#create data.yaml
create_data_yaml(class_path, data_path)

#model architecture
model = YOLO("yolo11s.pt")

#train model
train_model = model.train(data='/Users/inmka/PycharmProjects/ObjectDetection49022/data.yaml', epochs=40, imgsz=640)


