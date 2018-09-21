import cv2
import os

data_path = '/media/jeremy/Data/CloudStation/BehaviorDetection/mice_video_data'
image_path = '/media/jeremy/Data/CloudStation/BehaviorDetection/mice_extracted_images'

def video_to_images(name):
    os.chdir(data_path)
    video = cv2.VideoCapture(name)
    os.chdir(image_path)
    for i in range(0, 50000, 2000):     ## Keep frame every 2ms so that the mice had time to move around
        video.set(cv2.CAP_PROP_POS_MSEC,i) ## keep Frame at i ms
        ret, frame = video.read()
        cv2.imwrite(str(name) + "image-" +str(i) +".jpg", frame) ## write to disk the frame



files_name = os.listdir(data_path)

for i in files_name:
    video_to_images(i)
