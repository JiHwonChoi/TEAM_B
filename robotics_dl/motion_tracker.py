import rospy
import time
import sort_track.msg import IntList
import std_srvs.srv import SetBool
class Motiontracker():
    def __init__(self,tracker_topic,srv_mode = True):
        rospy.Subscriber(tracker_topic,IntList,self._track_cb)
        if srv_mode:
            rospy.wait_for_service('/motion_tracker/search_mode')
            print("Search mode detected")
            self.search_client = rospy.ServiceProxy('/motion_tracker/search_mode',SetBool)
        self.actor_idx = None #current actor_idx, it changes when its index change
        self.search_mode = False
        self.start_search = None
        self.endurance_time = time.time()
    def _track_cb(self,data):
        if self.search_mode:
            if time.time() - self.start_search >3:
                self.search_mode = False
                self.start_search = None
            else:
                search_fail = False
                if data.data==[]:
                    print("Search failed! Restart searching...")
                    search_fail = True
                else:
                    xmin,ymin,xmax,ymax,idx = data.data
                    if idx != self.actor_idx:
                        print("Another person detected! Restart searching...")
                        search_fail = True
                if search_fail:
                    self.start_search = time.time()
        else:
            if data.data == []:
                print("No Human found...")
                print("Move toward the rear camera to identify you")
                rospy.sleep(1)
            else:
                xmin,ymin,xmax,ymax,idx= data.data
                if self.actor_idx == idx:
                    self.endurance_time = time.time()
                    .publish('')



if __name__ == '__main__':
    rospy.init_node('motion_tracker')
    rate = rospy.Rate(10)
