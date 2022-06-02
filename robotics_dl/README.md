
# Implemetation for Robotics using Deep learning techniques

- 먼저 home directory에 있는 README에 있는 dependencies를 모두 설치해야합니다.

- Turtlebot3 관련 패키지들 중 "turtlebot3_navigation"과 "turtlebot3_description" 모두 해당 폴더에 있는 것으로 바꿔주세요. 

## Openpose를 이용한 넘어짐 감지 노드
pose_estimator.py 19줄에서 openpose_path를 openpose가 설치되어 있는 환경에 맞게 수정해주세요.

넘어짐 감지 & Emergency 서비스 서버에 전송 노드 실행
>python pose_estimator.py

## 서버로부터 목적지 좌표 수신 & 도착 sign 발신 노드

>python set_path_new.py

## 주행 노드
산책기능 ( Identification을 통한 트래킹 서비스) 활성화 (비활성화는 false를 argument로 줍니다.)

> python human_follower_with_motion_tracker.py --tracker_on true

## Node for face recognition (experimental)

> python face_recog.py



