#!/usr/bin/env python3

import rospy
from sebot_service.srv import GetImage, SetGoal

class Sebot:
    def __init__(self):
        rospy.init_node('sebot_info')
        
        self.image_msg = None



