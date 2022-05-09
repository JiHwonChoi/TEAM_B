TEAM_B

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

