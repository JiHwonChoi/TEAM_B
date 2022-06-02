

# TEAM_B Robot-Application Service for Nursing Home

### 요양원 로봇-어플리케이션 서비스

## Main Implementation

### 1. 사용자 어플리케이션을 통한 지정위치로 로봇 호출하기
### 2. 응급상황(넘어짐) 감지 & 어플리케이션을 통한 알림서비스
### 3. 야외 산책 기능 (사용자의 움직임을 트래킹하면서 interaction)



## Dependencies

- Openpose
- turtlebot3 & turtlebot3_msgs (https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/)
- Python 3.8
- ROS(Robot Operating System) noetic  (for Ubuntu 20.04) 

## 서버와의 웹소켓 연결
> rosluanch rosbridge_server rosbridge_websocket.launch

## 모든 로봇 관련 노드 활성화 (넘어짐 감지, Yolo+Depth, 산책 Tracking, 서버와의 통신 노드)

> chmod 777 main.sh

> ./main.sh

## 시뮬레이션 환경 활성화
> chmod 777 map.sh

> ./map.sh


## Gazebo simulation
Indoor map 과 outdoor map으로 구성되어 있습니다. 각각 capstone_turtlebot, outdoor_simulation 폴더(패키지)에서 world파일과 pgm파일을 확인하실수 있습니다.

launch indoor simulation
> roslaunch capstone_turtlebot capstone.launch

launch outdoor simulation
> roslaunch outdoor_simulation capstone_outdoor.launch


###  ** 로봇 관련 implementation은 robotics_dl 폴더 README 참고 **


## 파일 실행방법 
clone후 my-app 디렉토리에서 터미널을 켜고 


> npm install  
> npm start  


순으로 입력하면 됩니다. nodemodules 라는 폴더 설치 되는지 확인.  


## 소켓 테스트 용 앱 주의사항

src/Start.js 에서 useEffect() 함수 안에 있는 부분을 수정해야합니다.
F12로 콘솔창 열어서 서버랑 접속하는지 확인해주세요

### createProxyMiddleware 에러 났을경우
> npm install http-proxy-middleware --save-dev
