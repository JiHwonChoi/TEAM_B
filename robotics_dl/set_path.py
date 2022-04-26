import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry
from human_follower import Human_follower
from geometry_msgs.msg import Point,Pose,PoseStamped
from sebot_service.srv import *
import rospy
import numpy as np
PATH_A =np.array([(23.5,61.1),(25.7,65.6),(21.97,68.45),(16.48,74.68),(9.61,79.67),(0.935,83.29),(-9.23,85.02),(-18.49,82.40),(-16.947,77.188),(-13.6,72.56),(-8.87,66.47),(-5.758,63.45),(-2.63,63.67)])
goal_srv = '/goal_srv'
class Nav_goal_control:
    def __init__(self,start_pos,speed = 0.7,goal_threshold = 0.3,path = 'A'):
        self.MoveBaseClient = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.MoveBaseClient.wait_for_server()
        rospy.set_param('/move_base/DWAPlannerROS/max_vel_x', speed)
        rospy.set_param('/move_base/DWAPlannerROS/max_vel_y', speed)
        if path =='A':
            self.path= PATH_A
        elif path =='B':
            pass #Todo: make other paths...
        self.path=self.path-start_pos
        self.start_pos = start_pos
        self.sub = rospy.Subscriber("/odom",Odometry,self._odom_cb)
        self.goal = MoveBaseGoal()
        self._init_goal()
        self.cur_idx = 0
        self.goal_threshold = goal_threshold
        self.cur_pos = self.path[0]
        self.make_goal_pos(self.path[0][0],self.path[0][1])
        rospy.wait_for_service(goal_srv)
        print("Service detected")
        self.goal_client = rospy.ServiceProxy(goal_srv,SetGoal)
        goal = PoseStamped()
        goal.header.stamp = rospy.Time.now()
        goal.header.frame_id = 'map'
        goal.pose.position = Point(self.path[-1][0],self.path[-1][1],0)
        res = self.goal_client(goal)
        print("SERVICE STATUS NO",res.status)
    def _init_goal(self):
        self.goal.target_pose.header.frame_id = "map"
        self.goal.target_pose.header.stamp = rospy.Time.now()
    def check_goal(self):
        if self.cur_idx == len(self.path):
            return
        cur_dest = self.path[self.cur_idx]
        goal_dist = ((self.cur_pos[0]-cur_dest[0])**2 + (self.cur_pos[1]-cur_dest[1])**2)**0.5
        if goal_dist < self.goal_threshold:
            print ("We reach the checkpoint")
            if self.cur_idx+1 ==len(self.path):
                print("WE REACH THE FINAL DEST. END STROLLING.")
            else:
                next_dest =self.path[self.cur_idx+1]
                self.cur_idx+=1
                self.make_goal_pos(next_dest[0],next_dest[1])

    def make_goal_pos(self,x,y):
        self.goal.target_pose.pose.position.x = float(x)
        self.goal.target_pose.pose.position.y = float(y)
        self.goal.target_pose.pose.orientation.w = 1.0
        print("Sending goal")
        self.MoveBaseClient.send_goal(self.goal)
        #self.MoveBaseClient.wait_for_result()
        #print("GOAL RESULT",self.MoveBaseClient.get_result())
    def _odom_cb(self, data):
        x = data.pose.pose.position.x - self.start_pos[0]
        y = data.pose.pose.position.y - self.start_pos[1]
        self.cur_pos = [x,y]


if __name__=='__main__':
    rospy.init_node('set_path')
    print("INIT NODE")
    nav_control = Nav_goal_control((0,0),goal_threshold=5)
    #human_follower = Human_follower(False)
    while True:
        #print("ddd")
        nav_control.check_goal()
        #human_follower.modify_speed()
        rospy.sleep(1)