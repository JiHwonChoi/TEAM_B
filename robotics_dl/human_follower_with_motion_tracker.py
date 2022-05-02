import cv2
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist, Vector3, PoseWithCovariance, Pose, Point
from std_msgs.msg import Bool
from sort_track.msg import IntList
from detector import DetectorManager
import time
from visualization_msgs.msg import Marker, MarkerArray
from nav_msgs.msg import Odometry
from std_msgs.msg import ColorRGBA
import numpy as np
threshold_dist = 3.0
stop_threshold = 5.0
no_human_endurance_time = 3.0 # time to stop if there's no human
WIDTH = 960
HEIGHT = 540
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
        rospy.Subscriber('/sort_track_deep', IntList, self._track_cb,queue_size=1)
        self.actor_idx = None
        self.actor_depth = float('inf')
        self.endurance_time = time.time()
        self.last_data = [0,0,0,0,0,0]
    def _track_cb(self,data):
        print(data.data)
        if len(data.data)==0 or self.last_data == data.data:
            print("No Human found...")
            rospy.sleep(.5)
        else:
            xmin,ymin,xmax,ymax,depth,idx = data.data
            if self.actor_idx == int(idx) :
                self.endurance_time = time.time()
                #self.bbox = [xmin,ymin,width,height,depth]
                self.actor_depth = depth
                self.last_data = data.data
            _thres = 50

            if self.no_human_flag:
                if depth < threshold_dist:
                    #if human is in the center and close enough
                    if self.actor_idx is None or self.actor_idx == int(idx):
                        self.actor_idx = int(idx)
                        self.actor_depth = depth
                    else:
                        print("THERE MUST BE ONLY ONE PERSON toward camera for identification")
                        self.actor_idx = idx
                        self.actor_depth = depth
                else:
                    print("MOVE TO the CENTER AND COME NEARBY")


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
        if time.time() - self.endurance_time > no_human_endurance_time:
            self.no_human_flag = True
            self.actor_idx = None
            self.actor_depth = float('inf')

        if self.no_human_flag: #start searching
            _stop=Twist()
            _stop.angular.z = 0
            self.vel_pub.publish(_stop)
            print("We need to identify you. Please move toward the camera")
            rospy.sleep(5)
            print("SCAN FINISHED, actor idx",self.actor_idx)
            if self.actor_idx is not None:
                self.no_human_flag = False
                self.endurance_time = time.time()

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
                    print("YOU ARE TOO FAR AWAY... STOP FOR A SEC...",time.time())
                    _stop = Twist()
                    _stop.angular.z = 0
                    self.vel_pub.publish(_stop)

                else:
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
    human_follower=Human_follower(True)
    while True:
        human_follower.modify_speed()
        rospy.sleep(.1)
    rospy.spin()