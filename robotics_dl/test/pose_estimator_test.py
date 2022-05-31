import rospy
import sys
import cv2
import os
from sys import platform
import argparse
from sensor_msgs.msg import Image, CompressedImage
from std_msgs.msg import Bool
from std_srvs.srv import *
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from sebot_service.srv import GetImage
import time

HEIGHT = 540
WIDTH = 960
NECK_TH = 450 / 2

'''
-------PARAMETERS-----------
'''
openpose_path = '/home/danmuzi/openpose/'  # You need to change to dir where you download openpose
image_topic = '/rear_camera/rgb/image_raw'
emergency_srv = '/emergency_sign'
filename = '/home/danmuzi/flipping_video.mp4'
'''
--------------------------
'''

try:
    # Change these variables to point to the correct folder (Release/x64 etc.)
    sys.path.append(openpose_path + 'build/python');
    print(openpose_path + '/python')
    # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
    # sys.path.append('/usr/local/python')
    from openpose import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e
params = dict()
params["model_folder"] = openpose_path + "models/"
parser = argparse.ArgumentParser()
parser.add_argument("--image_path", default=openpose_path + "examples/media/COCO_val2014_000000000192.jpg",
                    help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
args = parser.parse_known_args()

# Add others in path?
for i in range(0, len(args[1])):
    curr_item = args[1][i]
    if i != len(args[1]) - 1:
        next_item = args[1][i + 1]
    else:
        next_item = "1"
    if "--" in curr_item and "--" in next_item:
        key = curr_item.replace('-', '')
        if key not in params:  params[key] = "1"
    elif "--" in curr_item and "--" not in next_item:
        key = curr_item.replace('-', '')
        if key not in params: params[key] = next_item

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()


class Pose_detector:
    def __init__(self, opWrapper, vis,srv_mode = False):
        #self.pose_sub = rospy.Subscriber(image_topic, Image, self._cb)
        self.comp_img_sub = rospy.Subscriber(image_topic + '/compressed', CompressedImage, self._comp_cb)
        self.opWrapper = opWrapper
        self.video = cv2.VideoCapture(filename)
        if self.video is None:
            print("VIDEO NOT FOUND")
        self.bridge = CvBridge()
        self.cnt = 0
        self.emergency_flag = False
        self._vis = vis
        out = cv2.VideoWriter('/home/danmuzi/outpy.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (WIDTH,HEIGHT))
        if srv_mode :
            rospy.wait_for_service(emergency_srv)
            print("Service detected")
            self.emergency_client = rospy.ServiceProxy(emergency_srv, GetImage)
        # print("GOGOGOOGOGOGO")
        while self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                self.__process_pose(frame,out)
                if  cv2.waitKey(25) & 0xFF == ord('q'):
                    out.release()
                    cv2.destroyAllWindows()
                    break
            else:
                #print("DONEENENENE")
                out.release()
                cv2.destroyAllWindows()
    def _comp_cb(self, data):
        # rospy.loginfo("RESPONSED")
        if self.emergency_flag:
            rospy.loginfo("RESPONSED")
            res = self.emergency_client(data)
            rospy.loginfo("SERVICE SUCCESS? : ", res.success)

    def __process_pose(self, imageToProcess,out):
        datum = op.Datum()
        datum.cvInputData = imageToProcess
        self.opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1.0
        # Display Image
        # print ("input",datum.cvInputData.shape)
        # print ("output", datum.cvOutputData.shape)

        ## x is index 0 , y(height) is index 1...
        emergency_flag = False
        _safe = True
        temp = datum.cvInputData.copy()
        # Todo:insert no detection sign
        try:
            for person in datum.poseKeypoints:
                # print("person detected")
                if person[1][1] == 0 or person[22][1] == 0:
                    continue

                if person[1][1] > NECK_TH:
                    # print ("person neck is over floor")
                    if person[8][0] == 0:
                        continue
                    angle = np.abs(np.arctan2(person[1][1] - person[8][1], person[1][0] - person[8][0])) * 180 / np.pi
                    # print ("angle",angle)
                    # print("person hip",person[8][1])
                    heap_angle = np.abs(np.arctan2(person[22][1] - person[8][1], person[22][0] - person[8][0])) * 180 / np.pi
                    print("angle", angle, " heap y", heap_angle)
                    if angle < 60 or angle > 120 or heap_angle < 60 or heap_angle >120:
                        _safe = False
                        cv2.putText(temp,"EMERGENCY DETECTED",(30, 30), font, fontScale, (0,0,255), 3 ,cv2.LINE_AA)
                        self.emergency_flag = True
                        # rospy.loginfo("People fall down! Emergency!")
            #rospy.loginfo(f"Emergency flag: {self.emergency_flag}")

            if _safe:
                self.emergency_flag = False
                # print("All people detected")

        except:
            self.emergency_flag = False  # Need more inspection...
            pass
        out.write(temp)
        if self._vis == True:
            cv2.imshow("OpenPose 1.7.0 - ROS_ROBOT_VERSION_BTEAM", temp)
            #cv2.imshow("Odd",datum.cvOutputdata)
            cv2.waitKey(25)


if __name__ == '__main__':
    rospy.init_node('sample_openpose')
    Pose_detector(opWrapper, vis=True)

    try:
        rospy.spin()

    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()





