#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import rospy
from sensor_msgs.msg import CompressedImage
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

class SeBot:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None

        self.qx = None
        self.qy = None
        self.qz = None
        self.qw = None

        self.img = None

        rospy.init_node('sebot_api')
        self.odom_subscriber = rospy.Subscriber("/odom", Odometry, self.odom_callback)
        self.image_subscrber = rospy.Subscriber("/camera/rgb/image_raw/compressed", CompressedImage, self.image_callback)
        self.goal_publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        # emergency_client
        # log subscriber
        # goal publisher

    def odom_callback(self, msg: Odometry):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.z = msg.pose.pose.position.z

        self.qx = msg.pose.pose.orientation.x
        self.qy = msg.pose.pose.orientation.y
        self.qz = msg.pose.pose.orientation.z
        self.qw = msg.pose.pose.orientation.w

    def image_callback(self, msg: CompressedImage):
        self.img = msg.data

    def publish_goal(self, goal):
        msg = PoseStamped()
        msg.header.frame_id = 'map'
        msg.pose.position.x = goal[0]
        msg.pose.position.y = goal[1]

        # need to optimize angle
        msg.pose.orientation.z = 1
        
        self.goal_publisher.publish(msg)

