import cv2
import numpy as np
try:
    from lamda.tflite import InstanceSegmentation, draw_segmented, create_opencl_delegate, create_cpu_delegate
except:
    print ("Please run this script in latest firerpa internal shell")
    exit(1)

image = cv2.imread("segmentation.png")

delegate = create_opencl_delegate()
segmenter = InstanceSegmentation(model="example_segmentation_model.tflite", delegate=delegate, min_area=8000, split=True)
results = segmenter.detect(image)

print("num instances:", len(results))
for box, score, class_id, class_name, mask, contours in results: print(class_id, class_name, float(score), mask.shape, len(contours))

segmented = draw_segmented(results, image)
cv2.imwrite("segmentation_output.jpg", segmented)