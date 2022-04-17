import face_recognition
import rospy
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from sensor_msgs.msg import Image, CompressedImage
import cv2

'''
------PARAMETERS-------
'''
image_topic = '/camera/rgb/image_raw'
actor_img_dir = 'actor_img/actor_1.png'

'''
-----------------------
'''



class Face_recognition:
    def __init__(self, actor_picture):  # actor_picture: dirs of actor_picture
        #self.image_sub = rospy.Subscriber('/camera/rgb/image_raw/compressed', CompressedImage, self._cb, queue_size=1)
        self.image_sub = rospy.Subscriber(image_topic, Image, self._cb, queue_size=1)
        self.actor_image = face_recognition.load_image_file(actor_picture[0])
        #self.actor_image1= face_recognition.load_image_file(actor_picture[1])
        # print("actor img",self.actor_image)
        self.actor_encoding = face_recognition.face_encodings(self.actor_image)[0]
        #self.actor_encoding1 = face_recognition.face_encodings(self.actor_image)[0]
        # print("actor encoding",self.actor_encoding)
        # cv2.imshow('actor_encoding',self.actor_encoding)
        # cv2.waitKey(1)
        self.bridge = CvBridge()
        # print("initialized")
        self.process_this_frame= 0
    def _cb(self, data):
        _r=1

        try:
             np_arr = np.fromstring(data.data, np.uint8)
             #self.cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
             #self.cv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
             self.cv_image = self.bridge.imgmsg_to_cv2(data, "rgb8")
             #print("cv_image type", type(self.cv_image[0][0][0]))
        except CvBridgeError as e:
            print(e)
        #print("go")
        resized_cv_image= cv2.resize(self.cv_image,(0,0), fx=1.0/_r, fy=1.0/_r)
        if self.process_this_frame == 0 :
            face_locations = face_recognition.face_locations(resized_cv_image,2,model='cnn')
            face_encodings = face_recognition.face_encodings(resized_cv_image)
            #print("face_loc",face_encodings)
            face_names = []
            #print("detected face", len(face_encodings))
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([self.actor_encoding], face_encoding)
                name = "Unknown"
                # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]
                print(matches)
                if matches[0] :
                    name= "Actor"
                face_names.append(name)
                #print("face_names", face_names)
                # Display the results
            print(face_names)
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top*=_r
                right*=_r
                bottom*=_r
                left*=_r
                # Draw a box around the face
                cv2.rectangle(self.cv_image, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                # cv2.rectangle(self.cv_image, (left, bottom + 70), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.cv_image, name, (left + 35, bottom + 35), font, 3.0, (0, 0, 255), 3)
            self.cv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_RGB2BGR)
            cv2.imshow('face_recog', self.cv_image)
            cv2.waitKey(1)
        self.process_this_frame = (self.process_this_frame + 1) % 2


if __name__ == '__main__':
    rospy.init_node('dd')
    fd = Face_recognition(actor_img_dir)
    rospy.spin()
