#!/usr/bin/env python3

import rospy
from sebot_service.srv import GetImage, SetGoal

class Sebot:
    def __init__(self):
        rospy.init_node('sebot_server')
        self.image_msg = None
        self.img_srv = rospy.Service("get_image", GetImage, self.get_image)
        while not rospy.is_shutdown():
            print(self.image_msg)

    def get_image(self, req):
        self.image_msg = req.image
        print(req.image)
        return True

s = Sebot()