import rospy
import sys
import cv2
import os
from sys import platform
import argparse
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
import numpy as np
import time
HEIGHT=1080
WIDTH=1920
NECK_TH=450
'''
-------PARAMETERS-----------
'''
openpose_path = '/home/danmuzi/openpose/' #You need to change to dir where you download openpose
image_topic= '/camera/rgb/image_raw'
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
params["model_folder"] = openpose_path+"models/"
parser = argparse.ArgumentParser()
parser.add_argument("--image_path", default=openpose_path+"examples/media/COCO_val2014_000000000192.jpg",
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
    def __init__(self,opWrapper):
        self.pose_sub=rospy.Subscriber(image_topic,Image,self._cb)
        self.opWrapper=opWrapper
        self.bridge=CvBridge()
        self.cnt=0

    def _cb(self,data):
        #print("hiihi")
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        self.__process_pose(cv_image)
    def __process_pose(self,imageToProcess):
        datum = op.Datum()
        datum.cvInputData = imageToProcess
        self.opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        #print("dd")
        # Display Image
        #print ("input",datum.cvInputData.shape)
        #print ("output", datum.cvOutputData.shape)

        ## x is index 0 , y(height) is index 1...
        emergency_flag=False

        #Todo:insert no detection sign
        try:
            for person in datum.poseKeypoints:
               if person[1][1]==0:
                   continue
               #print("neck: ",person[1][1])
               if person[1][1]>NECK_TH:
                   #print ("person neck is over floor")
                   if person[8][0]==0:
                       continue
                   angle=np.abs(np.arctan2(person[1][1]-person[8][1],person[1][0]-person[8][0]))*180/np.pi
                   print ("angle",angle)
                   if angle<30 or angle>150:
                       print("People fall down! Emergency!")

            #print("All people detected")
        except:
            cv2.imshow("OpenPose 1.7.0 - ROS_ROBOT_VERSION_BTEAM", datum.cvOutputData)
            cv2.waitKey(3)


if __name__ == '__main__':
    rospy.init_node('sample_openpose')
    Pose_detector(opWrapper)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()





