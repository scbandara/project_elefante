import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format
import cv2
import numpy as np
from firebase import firebase
import time
from checklight import checklightcondition
import firebase_admin
from firebase_admin import credentials, firestore

# firebase = firebase.FirebaseApplication('https://test-realtime-3b1ec.firebaseio.com/', None)
# firebase = firebase.FirebaseApplication('https://elefante-d2d6a-default-rtdb.firebaseio.com/', None)
# initialize sdk
# initialize sdk
cred = credentials.Certificate("flutterfiresamples-firebase-adminsdk-135oz-cbd1f9e298.json")
firebase_admin.initialize_app(cred)


namecam = input("enter  name: ")
latitude = input("enter latitude: ")
longitude = input("enter longitude: ")

# cap = cv2.VideoCapture(0)

# cap = cv2.VideoCapture("48.mp4")

# if cap is None or not cap.isOpened():
#   print('unable to open camera 1')
#   breakpoint()

# print('camera is connected wait ...')
# time.sleep(0.2)


WORKSPACE_PATH = 'Tensorflow/workspace'
APIMODEL_PATH = 'Tensorflow/models'
ANNOTATION_PATH = WORKSPACE_PATH + '/annotations'
MODEL_PATH = WORKSPACE_PATH + '/models'
CONFIG_PATH = MODEL_PATH + '/my_ssd_mobnet/pipeline.config'
CHECKPOINT_PATH = MODEL_PATH + '/my_ssd_mobnet/'
CUSTOM_MODEL_NAME = 'my_ssd_mobnet'

configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-11')).expect_partial()


def dem(score):
    score2 = score[0]
    print(score2)
    if score2 > 0.6:
        print("sent")
        # initialize firestore instance
        firestore_db = firestore.client()
        # add data
        firestore_db.collection(u'detections').add(
            {'time': time.ctime(), 'name': namecam, 'latitude': latitude, 'longitude': longitude})

        # data = {'time': time.ctime(), 'name': namecam, 'latitude': latitude, 'longitude': longitude}
        # result = firebase.post('test-realtime-3b1ec', data)
        # time.sleep(0.5)


@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH + '/label_map.pbtxt')

light1 = checklightcondition()

if light1 == 1:
    cap = cv2.VideoCapture("tee.mp4")
    # cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
if light1 == 0:
    cap = cv2.VideoCapture("rt.mp4")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cap.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # crr = frame
    # frame = (255-frame)
    if light1 == 0:
        frame = (255 - frame)

    image_np = np.array(frame)

    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}

    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()
    dem(detections['detection_scores'])

    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections,
        detections['detection_boxes'],
        detections['detection_classes'] + label_id_offset,
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=5,
        min_score_thresh=.75,
        agnostic_mode=False)

    cv2.imshow('object detection', cv2.resize(image_np_with_detections, (800, 600)))
    # cv2.imshow('s',frame)
    # cv2.imshow('s',crr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break
