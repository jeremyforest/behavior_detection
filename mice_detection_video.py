##Taken mostly from the example of object_detection

### In order for the script to run successfully (probleme with python path otehrwise I think) --> to run copy in '/models/research/object_detection' directory

### think about adding the following command from tensorflow/models/research/
### export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

from distutils.version import StrictVersion
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.
os.chdir('/media/jeremy/Data/CloudStation/BehaviorDetection/models/research/object_detection')
sys.path.append("..")
from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')

from utils import label_map_util
from utils import visualization_utils as vis_util

import cv2

## The model to use
MODEL_NAME = 'mice_inference_graph'

## Path to the model
#PATH_TO_FROZEN_GRAPH = '/' + MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_FROZEN_GRAPH = '/media/jeremy/Data/CloudStation/BehaviorDetection/models/research/object_detection/mice_inference_graph/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('/legacy/csv_data', 'behavior_detection.pbtxt')
PATH_TO_LABELS = '/media/jeremy/Data/CloudStation/BehaviorDetection/models/research/object_detection/legacy/csv_data/behavior_detection.pbtxt'
NUM_CLASSES = 1


## Load the frozen tensorflow model into memory
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

## Load the label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


PATH_TO_TEST_VIDEO_DIR = '/media/jeremy/Data/CloudStation/BehaviorDetection/mice_video_data_test'
TEST_VIDEO_PATHS = [os.path.join(PATH_TO_TEST_VIDEO_DIR, os.listdir(PATH_TO_TEST_VIDEO_DIR)[i]) for i in range(0, len(os.listdir(PATH_TO_TEST_VIDEO_DIR))) ]


cap = cv2.VideoCapture('/media/jeremy/Data/CloudStation/BehaviorDetection/mice_video_data_test/2015-10-12_14h27m25,377243s_V=1.avi')

def run_inference_for_single_image(image, graph):
      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
      return output_dict


### Need to update code to process video in batches instead of one at a time
with detection_graph.as_default():
    with tf.Session() as sess:
        while True:
             ret, image_np = cap.read()
             # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
             image_np_expanded = np.expand_dims(image_np, axis=0)
             # Actual detection.
             output_dict = run_inference_for_single_image(image_np, detection_graph)
             # Visualization of the results of a detection.
             vis_util.visualize_boxes_and_labels_on_image_array(
                  image_np,
                  output_dict['detection_boxes'],
                  output_dict['detection_classes'],
                  output_dict['detection_scores'],
                  category_index,
                  instance_masks=output_dict.get('detection_masks'),
                  use_normalized_coordinates=True,
                  line_thickness=2)

                """ymin = int((boxes[0][0][0]*height))
                xmin = int((boxes[0][0][1]*width))
                ymax = int((boxes[0][0][2]*height))
                xmax = int((boxes[0][0][3]*width))
                Result = np.array(img_np[ymin:ymax,xmin:xmax])"""

             cv2.imshow('object detection', cv2.resize(image_np, (640,480)))
             if cv2.waitKey(25) & 0xFF == ord('q'):
                 cv2.destroyAllWindows()
                 break
