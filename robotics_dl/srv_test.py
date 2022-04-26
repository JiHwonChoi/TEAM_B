import rospy
from std_srvs.srv import *
from sebot_service.srv import SetGoal,SetGoalResponse,GetImage, GetImageResponse
from geometry_msgs.msg import PoseStamped
emergency_srv = '/emergency_sign'
goal_srv = '/goal_srv'
#TUTORIAL FOR EMERGENCY SERVICE SERVER


def _handle_goal(req):
    try:
        print(req)
        return SetGoalResponse(1)
    except:
        return SetGoalResponse(0)


def _handle_image(req):
    try:
        print(req.shape)
        return SetGoalResponse(True)
    except:
        return SetGoalResponse(False)


if __name__=='__main__':
    p =input("E: Emergency test vs G: Goal test: ")
    rospy.init_node('server_tutorial')
    if p[0] == 'E':
        rospy.Service(emergency_srv, GetImage, _handle_image)
    elif p[0] == 'G':
        print("goal server init")
        rospy.Service(goal_srv,SetGoal,_handle_goal)
    else:
        print("Error")
    rospy.spin()