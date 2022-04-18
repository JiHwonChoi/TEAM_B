#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import rospy
from sensor_msgs.msg import CompressedImage
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult

class SeBot:
    def __init__(self):
        rospy.init_node('sebot_api', disable_signals=True)

        # robot pose
        self.x = None
        self.y = None
        self.z = None

        self.qx = None
        self.qy = None
        self.qz = None
        self.qw = None

        # robot image
        self.img = None
        
        # goal reached topic
        self.reached = -1

        # robot status => should be handled by flask
        self.idle = True

        # default path
        self.path = [[-0.615, 10.210], [-6.511, 10.224], [-8.757, -36.167], [1.814, -26.819]]
        self.path_couter = 0

        self.user_path = []

        
        self.odom_subscriber = rospy.Subscriber("/odom", Odometry, self.odom_callback)
        # self.image_subscrber = rospy.Subscriber("/camera/rgb/image_raw/compressed", CompressedImage, self.image_callback)
        self.goal_subscriber = rospy.Subscriber("/move_base/result", MoveBaseActionResult, self.result_callback)

        self.goal_publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=3)

        rospy.loginfo("SEBOT INITIALIZED")
        # emergency_client
        # log subscriber


    def run(self):
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            rate.sleep()
            if self.x is None or self.y is None:
                continue
            
            if self.idle:
                if self.reached == 0:
                    continue

                else:
                    rospy.loginfo("Sebot is IDLE")
                    if self.reached == -1:
                        self.path_couter = self.get_closest()

                    msg = self.make_goal(self.path[self.path_couter])

                    self.goal_publisher.publish(msg)
                    self.path_couter = (self.path_couter + 1) % 4
                    self.reached = 0

            else:
                if self.reached == 0:
                    continue

                else:
                    rospy.loginfo("Sebot is Active")
                    if len(self.user_path) == 0:
                        self.idle = True
                        self.reached = -1
                        continue

                    msg = self.make_goal(self.user_path[0])
                    self.goal_publisher.publish(msg)
                    self.user_path.pop(0)
                    self.reached = 0
        rospy.signal_shutdown("KEYBOARD INTERRUPT")

    def make_goal(self, point):
        msg = PoseStamped()
        msg.header.frame_id = "map"

        msg.pose.position.x = point[0]
        msg.pose.position.y = point[1]

        msg.pose.orientation.z = 1

        return msg


    def get_closest(self):
        closest_point = -1
        min_dist = None

        cur_point = [self.x, self.y]

        for i in range(len(self.path)):
            point = self.path[i]
            dist = (point[0] - cur_point[0])**2 + (point[1] - cur_point[1])**2

            if not min_dist:
                min_dist = dist
                closest_point = i
                continue

            elif min_dist > dist:
                min_dist = dist
                closest_point = i

        return closest_point


    def result_callback(self, msg: MoveBaseActionResult):
        if "Goal reached" in msg.status.text:
            self.reached = 1


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

