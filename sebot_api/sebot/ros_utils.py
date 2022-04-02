#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import rospy
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseGoal

class SeBot:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None

        self.qx = None
        self.qy = None
        self.qz = None
        self.qw = None

        rospy.init_node('sebot_api')
        odom_subscriber = rospy.Subscriber("odom", Odometry, self.odom_callback)
        #image subscrber
        #log subscriber
        #goal publisher

    def odom_callback(self, msg: Odometry):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.z = msg.pose.pose.position.z

        self.qx = msg.pose.pose.orientation.x
        self.qy = msg.pose.pose.orientation.y
        self.qz = msg.pose.pose.orientation.z
        self.qw = msg.pose.pose.orientation.w