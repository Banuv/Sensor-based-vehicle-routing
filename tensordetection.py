#code for object detection/count/write
#using tensor flow framework/libraries
import numpy as np
import tensorflow as tf
import cv2
import time
######added########################
import glob
import os
import csv
import heatmap
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
######################################

class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def processFrame(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        end_time = time.time()

        print("Elapsed Time:", end_time-start_time)

        im_height, im_width,_ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0,i,0] * im_height),
                        int(boxes[0,i,1]*im_width),
                        int(boxes[0,i,2] * im_height),
                        int(boxes[0,i,3]*im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        self.default_graph.close()

if __name__ == "__main__":
    model_path = '/home/banu/project_vehicle_routing/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
    odapi = DetectorAPI(path_to_ckpt=model_path)
    threshold = 0.7
#    cap = cv2.imread('/home/banu/project_vehicle_routing/input/2.jpg')
#    cap = [cv2.imread(file) for file in glob.glob('/home/banu/project_vehicle_routing/input/*.jpg')]

    files = glob.glob('/home/banu/project_vehicle_routing/input/*.jpg')


    open('heatmap.csv','w').close()

#    while True:
    #        r, img = cap.read()
    image_count = 0
    for f1 in files: 
        cap = cv2.imread(f1)
        print("filename:",f1) 
        
        img = cv2.resize(cap, (1280, 720))

        boxes, scores, classes, num = odapi.processFrame(img)

        # Visualization of the results of a detection.
        count = 0
        s1, s2, s3, s4 = 0, 0, 0, 0
        
        for i in range(len(boxes)):
            # Class 1 represents human
 #          if classes[i] == 1 and scores[i] > threshold:
            if classes[i] <= 90 and scores[i] > threshold:    
                box = boxes[i]
                print("box:", boxes[i])
                if box[1] < 320:
                   s1 = s1+1
                elif box[1] > 320 and box[1] < 640:
                   s2 = s2+1
                elif box[1] > 640 and box[1] < 960:
                   s3 = s3+1
                else:
                   s4 = s4+1
#                   print("s1,s2,s3,s4:", s1,s2,s3,s4)

                cv2.rectangle(img,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)
                count = count + 1
#        s1, s2, s3, s4 = 0, 0, 0, 0		

        cv2.imshow("preview", img)
        key = cv2.waitKey(500)
        print("count:", count)
        print("s1,s2,s3,s4:", s1,s2,s3,s4)

        csvData = [['0', image_count, s1], ['1', image_count, s2], ['2', image_count, s3], ['3', image_count, s4],['4', image_count, '0']]
  
        with open('heatmap.csv', 'a') as csvFile:
             writer = csv.writer(csvFile)
             writer.writerows(csvData)
        csvFile.close()
        s1, s2, s3, s4 = 0, 0, 0, 0
        image_count = image_count+1
     #   if key & 0xFF == ord('q'):
     #   break


    csvData = [['0', image_count, s1], ['1', image_count, s2], ['2', image_count, s3], ['3', image_count, s4],['4', image_count, '0']]
  
    with open('heatmap.csv', 'a') as csvFile:
         writer = csv.writer(csvFile)
         writer.writerows(csvData)
    csvFile.close()
    heatmap.main()

