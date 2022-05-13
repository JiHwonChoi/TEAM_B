import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry
from human_follower import Human_follower
from geometry_msgs.msg import Point,Pose,PoseStamped
from sebot_service.srv import *
import rospy
import numpy as np
goal_srv = '/goal_sign'
arrival_srv = '/arrival_sign'
class Nav_goal_control:
    def __init__(self,speed = 0.7,goal_threshold = 0.3,srv_mode = False):
        self.MoveBaseClient = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.MoveBaseClient.wait_for_server()
        rospy.set_param('/move_base/DWAPlannerROS/max_vel_x', speed)
        rospy.set_param('/move_base/DWAPlannerROS/max_vel_y', speed)
        self.dest = None
        self.sub = rospy.Subscriber("/odom",Odometry,self._odom_cb)
        self.goal = MoveBaseGoal()
        self.goal_threshold = goal_threshold
        self.cur_pos = None
        if srv_mode:
            rospy.Service(goal_srv,SetGoal,self._handle_goal)
            rospy.wait_for_service(arrival_srv)
            print("Service detected")
            self.arrival_client = rospy.ServiceProxy(arrival_srv,SendArrival)

    def _handle_goal(self,req):

        rospy.loginfo(req)
        x = req.goal.pose.position.x
        y = req.goal.pose.position.y

        self.make_goal_pos(x,y)
        return SetGoalResponse(True)

        # return SetGoalResponse(False)

    def check_goal(self):
        if self.dest is None:
            return
        try:
            goal_dist = ((self.cur_pos[0]-self.dest[0])**2 + (self.cur_pos[1]-self.dest[1])**2)**0.5
            print("goal_dist",goal_dist)
            if goal_dist < self.goal_threshold:
                rospy.loginfo ("We reach the checkpoint")
                res = self.arrival_client(True)
                rospy.loginfo(res.response)
                if not res.response:
                    rospy.loginfo("Arrival Server returns false... something wrong")
        except:
            rospy.loginfo("goal not specified")
    def make_goal_pos(self,x,y):
        self.goal.target_pose.header.frame_id = "map"
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.goal.target_pose.pose.position.x = float(x)
        self.goal.target_pose.pose.position.y = float(y)
        self.goal.target_pose.pose.orientation.w = 1.0
        rospy.loginfo("Sending goal")
        self.MoveBaseClient.send_goal(self.goal)
        #self.MoveBaseClient.wait_for_result()
        #print("GOAL RESULT",self.MoveBaseClient.get_result())
    def _odom_cb(self, data):
        x = data.pose.pose.position.x
        y = data.pose.pose.position.y
        self.cur_pos = [x,y]
        if self.dest is None:
            return
        goal_dist = ((self.cur_pos[0] - self.dest[0]) ** 2 + (self.cur_pos[1] - self.dest[1]) ** 2) ** 0.5
        print("goal_dist", goal_dist)
        if goal_dist < self.goal_threshold:
            rospy.loginfo("We reach the checkpoint")
            res = self.arrival_client(True)
            rospy.loginfo(res.response)
            if not res.response:
                rospy.loginfo("Arrival Server returns false... something wrong")


if __name__=='__main__':
    rospy.init_node('set_path')
    print("INIT NODE")
    nav_control = Nav_goal_control(goal_threshold=5,srv_mode=True)
    #human_follower = Human_follower(False)
    while True:
        #print("ddd")
        nav_control.check_goal()
        #human_follower.modify_speed()
        rospy.sleep(1)