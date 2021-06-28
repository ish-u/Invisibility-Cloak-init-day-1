import cv2

# importing the Coco Classname
classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as cocoNames:
    classNames = cocoNames.read().rstrip('\n').split('\n')


# importing the configuration files
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

# Required Settings
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# function that turn detected objects into white rectangles


def getFrame(videoCapture, visible):
    success, img = videoCapture.read()
    img = cv2.flip(img, 1)
    if visible:
        classIds, confs, bbox = net.detect(img, confThreshold=0.7)
        if len(classIds):
            for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
                if classId != 1:
                    cv2.rectangle(img, box, (255, 255, 255), -1)
                    cv2.putText(img, classNames[classId-1], (box[0] + (box[0]//2), box[1] + (box[1]//2)), cv2.FONT_HERSHEY_COMPLEX,
                                0.5, (0, 0, 0), 1)

    return success, img
