22.04.17
Dependencies
openpose (https://github.com/CMU-Perceptual-Computing-Lab/openpose)
yolov3_pytorch_ros (https://github.com/vvasilo/yolov3_pytorch_ros)
face_recognition(https://github.com/ageitgey/face_recognition)

Human Pose estimator with openpose:
You need to insert your directory to openpose in line 17! Checkout all parameters at the top of the script!
$ python pose_estimator.py

object detection with depth using yolov3:
Checkout all parameters at the top of the script!
I just use it by..
$ python detector.py --net_resolution 320x-1 (net resolution is to reduce memory usage...)

Face recognition:
Checkout all parameters at the top of the script!
python face_recog.py
