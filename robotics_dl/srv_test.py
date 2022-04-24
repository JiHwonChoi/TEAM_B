import rospy
from std_srvs.srv import *
emergency_srv = '/emergency_sign'
#TUTORIAL FOR EMERGENCY SERVICE CLIENT
if __name__=='__main__':
    rospy.wait_for_service(emergency_srv)
    print("Service detected")
    while True:
        try:
            client = rospy.ServiceProxy(emergency_srv,SetBool)
            res = client(True)
            print(res.success,res.message)
        except:
            pass