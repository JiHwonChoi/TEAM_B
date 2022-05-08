#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import rospy
import roslibpy
import base64
import numpy as np
import cv2
from sensor_msgs.msg import CompressedImage
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult

class SeBot:
    def __init__(self, db, robot_ip):
        #Init ros web socket
        self.client = roslibpy.Ros(host=robot_ip, port=9090)
        self.client.run()

        self.db = db

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
        
        # robot active step
        self.active_step = 0

        # default path
        self.path = [[-0.615, 10.210], [-6.511, 10.224], [-8.757, -36.167], [1.814, -26.819]]
        self.path_couter = 0

        self.user_path = []

        self.odom_subscriber = roslibpy.Topic(self.client, "odom", "nav_msgs/Odometry")
        self.odom_subscriber.subscribe(self.odom_callback)

        #Service
        # self.image_subscrber = rospy.Subscriber("/camera/rgb/image_raw/compressed", CompressedImage, self.image_callback)
        self.emergency_srv = roslibpy.Service(self.client, '/emergency_sign', 'sebot_service/GetImage')
        self.emergency_srv.advertise(self.upload_image)
        
        # Change it to service
        self.reach_subscriber = roslibpy.Topic(self.client, "move_base/result", "move_base_msgs/MoveBaseActionResult")
        self.reach_subscriber.subscribe(self.result_callback)
        
        rospy.loginfo(f'SEBOT INIT')

        # log subscriber


    def __del__(self):
        self.client.close()


    def upload_image(self, request, response):
        base64_bytes = request['image']['data'].encode('ascii')
        image_bytes = base64.b64decode(base64_bytes)
        res = self.db.image_upload(image_bytes)
        response['emergency'] = res
        return res


    # def run(self):
        # while not self.client.is_connected:
        #     time.sleep(1)
            
        #     if self.idle:
        #         if self.reached == 0:
        #             continue

        #         else:
        #             rospy.loginfo("Sebot is IDLE")
        #             if self.reached == -1:
        #                 self.path_couter = self.get_closest()

        #             msg = self.make_goal(self.path[self.path_couter])

        #             self.goal_publisher.publish(msg)
        #             self.path_couter = (self.path_couter + 1) % 4
        #             self.reached = 0

            # else:
            #     if self.reached == 0:
            #         continue

            #     else:
            #         rospy.loginfo("Sebot is Active")
            #         if len(self.user_path) == 0:
            #             self.idle = True
            #             self.reached = -1
            #             continue

            #         msg = self.make_goal(self.user_path[0])
            #         self.goal_publisher.publish(msg)
            #         self.user_path.pop(0)
            #         self.reached = 0

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


    def result_callback(self, msg):
        if "Goal reached" in msg["status"]["text"]:
            self.reached = 1


    def odom_callback(self, msg):
        self.x = msg["pose"]["pose"]["position"]["x"]
        self.y = msg["pose"]["pose"]["position"]["y"]
        self.z = msg["pose"]["pose"]["position"]["z"]

        self.qx = msg["pose"]["pose"]["orientation"]["x"]
        self.qy = msg["pose"]["pose"]["orientation"]["y"]
        self.qz = msg["pose"]["pose"]["orientation"]["z"]
        self.qw = msg["pose"]["pose"]["orientation"]["w"]


    def image_callback(self, msg: CompressedImage):
        self.img = msg.data

