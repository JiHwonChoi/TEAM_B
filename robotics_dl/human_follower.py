import cv2
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist, Vector3, PoseWithCovariance, Pose, Point
from std_msgs.msg import Bool
from detector import DetectorManager
import time
from visualization_msgs.msg import Marker, MarkerArray
from nav_msgs.msg import Odometry
from std_msgs.msg import ColorRGBA
import numpy as np


threshold_dist = 3.0
stop_threshold = 5.0
no_human_endurance_time = 5.0 # time to stop if there's no human


class Human_follower(DetectorManager):
    def __init__(self, follower_mode=False,speed = 0.5):
        super().__init__()
        self.flag=follower_mode
        self.no_human_flag = False
        self.cmd_vel = rospy.Subscriber('/cmd_vel_raw',Twist,self._vel_cb,queue_size=1)
        self.max_vel_x = speed
        self.max_vel_y = speed
        rospy.set_param('/move_base/DWAPlannerROS/max_vel_x', speed)
        rospy.set_param('/move_base/DWAPlannerROS/max_vel_y', speed)
        self.max_speed = (self.max_vel_x ** 2 + self.max_vel_y ** 2) ** 0.5
        #self.odom = rospy.Subscriber('/odom', Odometry, self._odom_cb,queue_size=1)
        self.odom_idx=0
        self.vel_pub = rospy.Publisher('/cmd_vel',Twist,queue_size=1)
        self.no_human_pub = rospy.Publisher('/human_follower/no_human',Empty,queue_size=1)
        #self.marker_pub = rospy.Publisher('/actor_loc',Marker)

    def _vel_cb(self,data):
        self.linear = data.linear
        self.angular = data.angular

    def modify_speed(self):
        pub_vel = Twist()
        if not self.flag:
            try:
                pub_vel.linear = self.linear
                pub_vel.angular = self.angular
                self.vel_pub.publish(pub_vel)
            except:
                #print("Robot currently stop.")
                pass
            return
        if self.depth_point is None:
            if self.no_human_flag == False:
                self.no_human_flag = time.time()
            elif time.time() - self.no_human_flag > no_human_endurance_time:
                print("We cannot FIND YOU, STOP!")
                self.vel_pub.publish(Twist())
                self.no_human_pub.publish(Bool(True))
                return
        else:
            self.no_human_flag = False

        if self.depth_point is None or self.depth_point<threshold_dist :
            try:
                pub_vel.linear = self.linear
                pub_vel.angular = self.angular
                self.vel_pub.publish(pub_vel)
            except:
                #print("Robot currently stop.")
                pass

        else:
            try:
                linear = self.linear
                angular = self.angular
                print ("depth point",self.depth_point)
                if self.depth_point > stop_threshold:
                    print("WE LOST YOU OR YOU ARE TOO FAR AWAY... STOP FOR A SEC...",time.time())
                    self.vel_pub.publish(Twist())
                else:
                    #cur_speed = (self.linear.x ** 2 + self.linear.y ** 2) ** 0.5
                    speed_ratio = threshold_dist/self.depth_point # positive value: the actor is far from robot, you need to slow down
                    print("speed_ratio",speed_ratio)
                    linear.x = min( self.max_vel_x,speed_ratio * linear.x)
                    linear.y = min( self.max_vel_y,speed_ratio * linear.y)
                    pub_vel.linear = linear
                    pub_vel.angular = angular
                    self.vel_pub.publish(pub_vel)
            except:
                print("No Linear & Angular values")



if __name__ == '__main__':
    rospy.init_node("human_follower")
    human_follower=Human_follower(False)
    while True:
        print("it")
        human_follower.modify_speed()
        rospy.sleep(.1)
    rospy.spin()