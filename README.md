# behavior_detection

Running on Ubuntu 16.04.

[X] Mice detection
	[X] On video
		[] Need to validate
	[] Real time = implement on GPU ?
[] Mice behavior categorisation
	[] Sniffing tea ball versus other behavior
	[] Other behavior implementation (rearing, grooming ...).

Using tensorflow object detection API to do mice detection. Then the idea I'm developing right now is to use only the detected mice within its bounding box portion of the image and put that througt a CNN for behavior categorisation.


How to run :

This project make use of the mobilenet_v2 model trained on the coco dataset and use transfer learning with custom labelled images to perform mice detection. All the images used for learning were previously extracted from acquired video (using the "data extraction.py" script). 

To reproduce the results, you need to run the "xml to csv.py" script and then generate the tf record using the "generate tfrecord.py" script.

Training the model is done using the tensorflow object detection API.

Then run "mice detection.py" for images or "mice detection video.py" for detection in videos.



Works well on images. Also works on videos but at low fps. Will need to try to run it on GPU to see if I can perform real time. Also maybe use threading to buffer frames with OpenCV like here https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/ ??
