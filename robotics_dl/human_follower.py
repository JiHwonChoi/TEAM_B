import cv2
import rospy
class Human_follower:
    def __init__(self):
        self.front_camera = rospy.Subscriber('camera/rgb/image_raw',Image,self._cb,que)