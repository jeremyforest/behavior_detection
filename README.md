# behavior_detection

Running on Ubuntu 16.04.
Using tensorflow/model/object_detection


Detection of mice during behavioral experiment.
Used mobilenet_v2 trained on the coco dataset and used transfer learning with custom labelled images to perform mice detection.
Works well on images.
Now also works on videos but at low fps. Will need to try to run it on GPU to see if I can perform real time. Also maybe use threading to buffer frames with OpenCV like here https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/ ??
