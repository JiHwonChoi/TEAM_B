import rospy
from std_srvs.srv import *
from sebot_service.srv import *
from geometry_msgs.msg import PoseStamped
emergency_srv = '/emergency_sign'
goal_srv = '/goal_sign'
arrival_srv = '/arrival_sign'
#TUTORIAL FOR EMERGENCY SERVICE SERVER


def _handle_goal(req):
    try:
        rospy.loginfo("Arrival succeeded")
        return SendArrivalResponse(True)
    except:
        return SendArrivalResponse(False)


def _handle_image(req):
    try:
        print(req.shape)
        return SetGoalResponse(True)
    except:
        return SetGoalResponse(False)


if __name__=='__main__':
    rospy.init_node('server_tutorial')
    rospy.Service(arrival_srv,SendArrival,_handle_goal)
    rospy.wait_for_service(goal_srv)
    rospy.loginfo("Service detected")
    req = SetGoalRequest()
    req.goal.pose.position.x = 5
    req.goal.pose.position.y = 60
    rospy.loginfo("GOAL SENT")
    goal_client = rospy.ServiceProxy(goal_srv,SetGoal)
    res = goal_client(req)
    rospy.loginfo(res)

    rospy.spin()