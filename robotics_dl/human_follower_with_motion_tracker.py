import cv2
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist, Vector3, PoseWithCovariance, Pose, Point
from std_msgs.msg import Bool
from yolov3_pytorch_ros.msg import BoundingBoxes,BoundingBox
from sort_track.msg import IntList
from detector import DetectorManager
import time
from visualization_msgs.msg import Marker, MarkerArray
from nav_msgs.msg import Odometry
from std_msgs.msg import ColorRGBA
from cv_bridge import CvBridge
from sebot_service.srv import GetImage
from sensor_msgs.msg import Image, CompressedImage
import cv2
import numpy as np
threshold_dist = 3.0
stop_threshold = 5.0
no_human_endurance_time = 6.0 # time to stop if there's no human
WIDTH = 960
HEIGHT = 540
emergency_srv = '/emergency_sign'
image_topic = '/rear_camera/rgb/image_raw'
class Human_follower(DetectorManager):
    def __init__(self, follower_mode=False,speed = 0.5, theta = 0.2):
        super().__init__(False)
        self.flag=follower_mode
        self.no_human_flag = False
        self.cmd_vel = rospy.Subscriber('/cmd_vel_raw',Twist,self._vel_cb,queue_size=1)
        self.max_vel_x = speed
        self.max_vel_y = speed
        rospy.set_param('/move_base/DWAPlannerROS/max_vel_x', speed)
        rospy.set_param('/move_base/DWAPlannerROS/max_vel_y', speed)
        rospy.set_param('/move_base/DWAPlannerROS/min_vel_theta',speed)
        rospy.set_param('/move_base/clearing_rotation_allowed', False)
        rospy.set_param('/move_base/recovery_behavior_enabled', False)
        self.max_speed = (self.max_vel_x ** 2 + self.max_vel_y ** 2) ** 0.5
        #self.odom = rospy.Subscriber('/odom', Odometry, self._odom_cb,queue_size=1)
        self.odom_idx=0
        self.vel_pub = rospy.Publisher('/cmd_vel',Twist,queue_size=1)
        rospy.Subscriber('/sort_track_deep', IntList, self._track_cb,queue_size=1)
        rospy.Subscriber('/sort_vis',Image,self._vis_cb,queue_size=10)
        self.track_pub = rospy.Publisher('/track_pub',Image,queue_size=1)
        self.actor_idx = None
        self.comp_img_sub = rospy.Subscriber(image_topic + '/compressed', CompressedImage, self._comp_cb)
        self.actor_depth = float('inf')
        self.endurance_time = time.time()
        self.last_data = [0,0,0,0,0,0]
        self.vis_img = None
        self.bridge = CvBridge()
        self.initial_endurance = time.time()
        self.linear = Vector3(0,0,0)
        self.angular = Vector3(0,0,0)
        self.vis_img_for_pub = None
        rospy.wait_for_service(emergency_srv)
        print("Service detected")
        self.emergency_client = rospy.ServiceProxy(emergency_srv, GetImage)
        self.comp_data = None
        self.last_service_time = 0
    def _comp_cb(self, data):
        self.comp_data = data
        #rospy.loginfo(self.no_human_flag)
        if self.no_human_flag and time.time() - self.last_service_time > 3:
            rospy.loginfo("REUESTING")
            res = self.emergency_client(self.comp_data)
            rospy.loginfo("SERVICE SUCCESS? : ", res.success)
            if res.success:
                self.last_service_time = time.time()
    def _vis_cb(self,data):
        self.vis_img = self.bridge.imgmsg_to_cv2(data, "8UC3")
        #self.vis_img_for_pub = self.vis_img
        #rospy.loginfo(type(self.vis_img_for_pub))
        try:
            cv2.imshow('track_result', self.vis_img_for_pub)
            cv2.waitKey(25)
    def __get_human_depth(self,bbox):
        rospy.loginfo(len(self.detection_results.bounding_boxes))

        for detection_result in self.detection_results.bounding_boxes:
            #rospy.loginfo(f"detection_result {np.abs(int(detection_result.xmin - bbox[0])) <= 2 and np.abs(int(detection_result.ymax - bbox[3]))}")
            #rospy.loginfo(f"loss {int(detection_result.xmin - bbox[0])} , {detection_result.ymax - bbox[3]}")
            if np.abs(int(detection_result.xmin - bbox[0])) <= 2 and np.abs(int(detection_result.ymax - bbox[3])) <=2:
                #rospy.loginfo(detection_result.depth)
                return detection_result.depth

    def _track_cb(self,data):
        #print(data.data)
        vis_img = self.vis_img
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1.0
        thickness = int(3)
        #
        if len(data.data)==0 or self.last_data == data.data:
            #rospy.loginfo("No Human found...")
            cv2.putText(vis_img,"Move toward to identify you.",(50,50),font,fontScale,(255,255,0),thickness,cv2.LINE_AA)
            rospy.sleep(.5)
        else:
            #rospy.loginfo("Human Recognized")
            xmin,ymin,xmax,ymax,_,idx = data.data
            _thres = 50
            depth = self.__get_human_depth([xmin,ymin,xmax,ymax])
            if not self.no_human_flag and self.actor_idx == int(idx) :
                self.endurance_time = time.time()

                self.last_data = data.data
            elif not self.no_human_flag:
                # cv2.putText(vis_img, f"Target_actor: {self.actor_idx}, Depth:{np.round(self.actor_depth, 3)}",
                #             (50, HEIGHT - 50), font, fontScale, (255, 255, 0), thickness, cv2.LINE_AA)
                cv2.putText(vis_img, f"Target_actor: {self.actor_idx}",
                                         (50, HEIGHT - 50), font, fontScale, (255, 255, 0), thickness, cv2.LINE_AA)
                # print("vis_img",vis_img)
                rospy.loginfo(type(vis_img))
                self.track_pub.publish(self.bridge.cv2_to_imgmsg(vis_img,"bgr8"))
                self.vis_img_for_pub = self.vis_img

                pass
            else:
                if depth < threshold_dist and depth != -1 and depth!= 0:
                    #if human is in the center and close enough
                    if self.actor_idx is None:
                        self.actor_idx = int(idx)
                        self.actor_depth = depth

                    elif self.actor_idx != int(idx) and depth < self.actor_depth:
                        _word = "THERE MUST BE ONLY ONE PERSON toward camera for identification"
                        rospy.loginfo(_word)
                        cv2.putText(vis_img, _word, (50, 50), font, fontScale, (255, 255, 0), thickness, cv2.LINE_AA)
                        self.actor_idx = int(idx)
                        self.actor_depth = depth
                    else:
                        pass
                else:
                    _word = "MOVE TO the CENTER AND COME NEARBY"
                    #rospy.loginfo("MOVE TO the CENTER AND COME NEARBY")
                    cv2.putText(vis_img, _word, (50, 50), font, fontScale, (255, 255, 0), thickness, cv2.LINE_AA)
        #cv2.putText(vis_img,f"Target_actor: {self.actor_idx}, Depth:{np.round(self.actor_depth,3w)}",(50,HEIGHT-50),font,fontScale,(255,255,0),thickness,cv2.LINE_AA)
        cv2.putText(vis_img, f"Target_actor: {self.actor_idx}",
                    (50, HEIGHT - 50), font, fontScale, (255, 255, 0), thickness, cv2.LINE_AA)
        #print("vis_img",vis_img)
        self.track_pub.publish(self.bridge.cv2_to_imgmsg(vis_img, "bgr8"))
        self.vis_img_for_pub = self.vis_img


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
            rospy.loginfo("Timeout! We Lost the actor.")
            #if time.time() - self.initial_endurance > no_human_endurance_time *2:
            #rospy.loginfo("Initial is happened.")
            if (self.linear.x != 0 or self.linear.y != 0) or self.angular.z == 0:
                self.no_human_flag = True
                self.actor_idx = None
                self.actor_depth = float('inf')
            else:
                try:
                    rospy.loginfo("CIRCULATING...")
                    _vel = Twist()
                    _vel.linear = self.linear
                    _vel.angular = self.angular
                    self.vel_pub.publish(_vel)
                except:
                    rospy.loginfo("Something wrong with circulating" )
                return
        if self.no_human_flag: #start searching
            _stop = Twist()
            _stop.angular.z = 0
            self.vel_pub.publish(_stop)
            print("We need to identify you. Please move toward the camera")
            rospy.sleep(5)
            print("SCAN FINISHED, actor idx",self.actor_idx)
            if self.actor_idx is not None:
                self.no_human_flag = False
                self.endurance_time = time.time()
                self.initial_endurance = time.time()

        if self.depth_point is None:
            _stop = Twist()
            _stop.angular.z =0
            self.vel_pub.publish(_stop)

        elif self.depth_point < threshold_dist :
            try:
                pub_vel.linear = self.linear
                pub_vel.angular = self.angular
                self.vel_pub.publish(pub_vel)
            except:
                #print("Robot currently stop.")
                pass
        else:
            linear = self.linear
            angular = self.angular
            #print ("depth point",self.depth_point)
            if self.actor_depth > stop_threshold:
                rospy.loginfo("YOU ARE TOO FAR AWAY... STOP FOR A SEC...")
                _stop = Twist()
                _stop.angular.z = 0
                self.vel_pub.publish(_stop)

            else:
                print("actor_depth", self.actor_depth)
                try:
                    speed_ratio = threshold_dist/self.actor_depth # positive value: the actor is far from robot, you need to slow down
                    #print("speed_ratio",speed_ratio)
                    linear.x = min( self.max_vel_x,speed_ratio * linear.x)
                    linear.y = min( self.max_vel_y,speed_ratio * linear.y)
                    pub_vel.linear = linear
                    pub_vel.angular = angular

                    self.vel_pub.publish(pub_vel)
                except:
                    rospy.loginfo("actor_depth is zero")


if __name__ == '__main__':
    rospy.init_node("human_follower")
    human_follower=Human_follower(False)
    while True:
        human_follower.modify_speed()
        rospy.sleep(.1)
    rospy.spin()