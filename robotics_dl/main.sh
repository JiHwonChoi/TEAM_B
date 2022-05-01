#!/bin/bash
source /home/danmuzi/catkin_ws/devel/setup.bash
tmux new-session -d -s human_follower 'python human_follower.py'
tmux split-window -v -p 20
tmux new-session -d -s pose_estimator 'python pose_estimator.py --net_resolution 320x-1'
