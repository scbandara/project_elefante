import cv2
from firebase import firebase
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import time

firebase = firebase.FirebaseApplication('https://test-realtime-3b1ec.firebaseio.com/', None)

namecam = input("Enter a name: ")
latitude = input("Enter latitude: ")
longitude = input("Enter longitude: ")


def resfilter(c1, pred1):
    if c1 == 'Indian_elephant' or c1 == 'tusker' or c1 == 'African_elephant':
        return c1, pred1 * 100
        pried2 = pred1 * 100
        if pred1 > 0.1:
            sendmsg()
            print('sent')


# Load the cascade
e_cascade = cv2.CascadeClassifier('cascade.xml')
elecascade = cv2.CascadeClassifier('cascade22.xml')
# To capture video from webcam.

# cap = cv2.VideoCapture(0)

cap = cv2.VideoCapture("48.mp4")

if cap is None or not cap.isOpened():
    print('unable to open camera 1')
    breakpoint()

print('camera is connected wait ...')
time.sleep(0.2)

# To use a video file as input
# cap = cv2.VideoCapture('Wildelephant.mp4')
# firebase = firebase.FirebaseApplication('https://test-realtime-3b1ec.firebaseio.com/', None)
count = 0

flag = 1
flag2 = 0

crop_img = 255 * np.ones(shape=[224, 224, 3], dtype=np.uint8)
model = ResNet50(weights='imagenet')

if flag == 1:
    while True:
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the elephants
        test1 = e_cascade.detectMultiScale(gray, 1.1, 4)
        ele = elecascade.detectMultiScale(gray, 1.1, 4)
        # print('sampled')
        # print (len(test1))
        # Draw the rectangle around each elephant
        for (x, y, w, h) in test1:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if len(test1) > 0:
                crop_img = img[y:y + h, x:x + w]
                print(" ")

            else:
                print('no elephant')

            flag2 = 1

        if count == 10:
            if len(test1) > 0:
                print(" ")
                data = {'time': time.ctime(), 'name': namecam, 'latitude': latitude, 'longitude': longitude}
                result = firebase.post('test-realtime-3b1ec', data)
                # time.sleep(0.7)
            else:
                print('no elephant')

            count = 0

        for (x, y, w, h) in ele:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # time.sleep(0.2)
        # Convert to grayscale

        width = 224
        height = 224
        dim = (width, height)

        # resize image
        crop_img = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)

        img_path = crop_img
        # img =(img_path, target_size=(224, 224))
        x = image.img_to_array(crop_img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x)

        # print('Predicted:', decode_predictions(preds, top=3)[0])
        # Predicted: [(u'n02504013', u'Indian_elephant', 0.82658225), (u'n01871265', u'tusker', 0.1122357), (u'n02504458', u'African_elephant', 0.061040461)]

        # print('Predicted:', decode_predictions(preds, top=3)[0])
        # Predicted: [(u'n02504013', u'Indian_elephant', 0.82658225), (u'n01871265', u'tusker', 0.1122357), (u'n02504458', u'African_elephant', 0.061040461)]


        mylist = (decode_predictions(preds, top=3)[0])

        newlist = []
        for item in mylist:
            # print(item)

            cat = (resfilter(item[1], item[2]))
            print(cat)
            #   print(item[2])

            if '-' in item[0]:
                item = tuple(item[0].split(' - '))
            newlist.append(item)

        #     print(newlist)

        # time.sleep(0.1)
        cv2.imshow('img', img)
        cv2.imshow("cropped", crop_img)

        count += 1
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    # Release the VideoCapture object
    cap.release()

#
#
#
# img = cv2.imread("lenna.png")
# crop_img = img[y:y+h, x:x+w]
# cv2.imshow("cropped", crop_img)

else:
    print("flag")
