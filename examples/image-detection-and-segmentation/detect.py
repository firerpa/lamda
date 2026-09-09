import cv2
import numpy as np
try:
    from lamda.tflite import ObjectDetection, draw_detected, create_opencl_delegate, create_cpu_delegate
except:
    print ("Please run this script in latest firerpa internal shell")
    exit(1)

image = cv2.imread("detection.png")


classes = ['乌龟', '企鹅', '伞', '兔子', '冰激凌', '凤梨', '包', '南瓜', '吉他', '大象', '太阳花', '宇航员', '帐篷', '帽子', '房子', '挂锁', '杯子', '松鼠', '枕头', '树', '树袋熊', '椅子', '气球', '汉堡包', '熊猫', '玫瑰花', '瓢虫', '瓶子', '电话', '皇冠', '篮子', '耳机', '花盆', '苹果', '草莓', '蘑菇', '蛋糕', '蝴蝶', '裙子', '账篷', '足球', '车', '轮胎', '铲土机', '闹钟', '鞋', '马', '鱼', '鸟', '鸭子']

delegate = create_opencl_delegate()
detector = ObjectDetection(model="example_detection_model.tflite", delegate=delegate, confidence=0.8, iou=0.45, classes=classes)
results = detector.detect(image)

for bound, confidence, class_id, name in results: print("confidence:", confidence, "class:", class_id, "name:", name)

segmented = draw_detected(results, image)
cv2.imwrite("detection_output.jpg", segmented)