#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import rospy
import roslibpy
import base64
import time

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

        # goal reached topic
        self.arrival = False

        # robot status => should be handled by flask
        self.idle = True
        
        # robot active step
        self.active_step = 0

        # default path
        self.path = [[-0.615, 10.210], [-6.511, 10.224], [-8.757, -36.167], [1.814, -26.819]]
        self.path_counter = 0

        self.user_path = []
        self.user_id = None

        # Robot Odom Topic
        self.odom_subscriber = roslibpy.Topic(self.client, "odom", "nav_msgs/Odometry")
        self.odom_subscriber.subscribe(self.odom_callback)

        # Robot Emergency Service
        self.emergency_srv = roslibpy.Service(self.client, '/emergency_sign', 'sebot_service/GetImage')
        self.emergency_srv.advertise(self.upload_image)
        
        # Robot Arrival Service
        self.arrival_srv = roslibpy.Service(self.client, "/arrival_sign", "sebot_service/SendArrival")
        self.arrival_srv.advertise(self.get_arrival)
        
        # Robot Destination Service
        self.goal_srv = roslibpy.Service(self.client, "/goal_sign", "sebot_service/SetGoal")
        # ros_request = roslibpy.ServiceRequest({"goal": {
        #             "header": {"frame_id": "map"},
        #             "pose": {"position": {"x": self.path[self.path_counter][0], "y": self.path[self.path_counter][1]},
        #                     "orientation": {"w": 1}
        #                     }
        #         }})
        # result = self.goal_srv.call(ros_request)
        # self.path_counter = (self.path_counter + 1) % (len(self.path))
        # Call Once when Init

        rospy.loginfo(f'SEBOT INIT Successfully')

        # log subscriber


    def __del__(self):
        self.client.close()

    def get_arrival(self, request, response):
        if request['arrival'] == True:
            self.arrival = True
            response['response'] = True

        #     # if self.idle:
        #     #     ros_request = roslibpy.ServiceRequest({"goal": {
        #     #         "header": {"frame_id": "map"},
        #     #         "pose": {"position": {"x": self.path[self.path_counter][0], "y": self.path[self.path_counter][1]},
        #     #                 "orientation": {"w": 1}
        #     #                 }
        #     #     }})
        #     #     result = self.goal_srv.call(ros_request)

        #     #     if result['response']:
        #     #         self.path_counter = (self.path_counter + 1) % (len(self.path))

        #     #     response = response & result['response']
        # print(response)
        return True


    def upload_image(self, request, response):
        base64_bytes = request['image']['data'].encode('ascii')
        image_bytes = base64.b64decode(base64_bytes)
        res = self.db.image_upload(image_bytes)
        response['emergency'] = res
        return True


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


    def odom_callback(self, msg):
        self.x = msg["pose"]["pose"]["position"]["x"]
        self.y = msg["pose"]["pose"]["position"]["y"]
        self.z = msg["pose"]["pose"]["position"]["z"]

        self.qx = msg["pose"]["pose"]["orientation"]["x"]
        self.qy = msg["pose"]["pose"]["orientation"]["y"]
        self.qz = msg["pose"]["pose"]["orientation"]["z"]
        self.qw = msg["pose"]["pose"]["orientation"]["w"]
        # print(self.x, self.y, self.z)
