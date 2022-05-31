#!/bin/bash
source /home/danmuzi/catkin_ws/devel/setup.bash
tmux new-session -d

tmux split-window -h
tmux select-pane -L
tmux split-window -v
tmux split-window -h
tmux select-pane -t 0
tmux send "cd robotics_dl" C-m
tmux send "source ~/catkin_ws/devel/setup.bash" C-m
tmux send "conda activate capstone" C-m
tmux send "python human_follower_with_motion_tracker.py" C-m
tmux select-pane -t 1
tmux send "cd robotics_dl" C-m
tmux send "source ~/catkin_ws/devel/setup.bash" C-m
tmux send "conda activate capstone" C-m
tmux send "python pose_estimator.py --net_resolution 320x-1" C-m
tmux select-pane -t 2
tmux send "cd robotics_dl" C-m
tmux send "source ~/catkin_ws/devel/setup.bash" C-m
tmux send "conda activate capstone" C-m
tmux send "python set_path_new.py" C-m
tmux select-pane -t 3
tmux send "cd robotics_dl" C-m
tmux send "source ~/catkin_ws/devel/setup.bash" C-m
tmux send "conda activate capstone" C-m
tmux send "roslaunch sort_track sort_deep.launch" C-m
tmux attach-session -d