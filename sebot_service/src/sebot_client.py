#!/usr/bin/env python3

import rospy
from sebot_service.srv import GetImage, SetGoal
from sensor_msgs.msg import CompressedImage, Image



if __name__=="__main__":
    rospy.init_node("client", anonymous=True, disable_signals=True)

    img = rospy.wait_for_message("/camera/rgb/image_raw/compressed", CompressedImage)
    # print(img)
    rospy.wait_for_service("/get_image")

    
    get_image = rospy.ServiceProxy("/get_image", GetImage)
    res = get_image(img)
    print(res.success)