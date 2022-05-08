import React, {useState, useEffect} from 'react'
import './start.css'
import New from './New';
import Homelogo from './Homelogo';
import Search from './Search';
import Home from './Home';
import Notification from './Notification';
import Profile from './Profile';
import Navigation from './Navigation';
import axios from 'axios';
import io from 'socket.io-client'





function Start (props) {
        
        const [article, setArticle] = useState(<Homelogo />)
        const [title, setTitle] = useState('소켓통신 실패')
        
        //api 지속적으로 새로고침 하는 함수 
        //socket 안되면 이걸로라도
        const getapi  = async () => {

                
                // let title = response
                // setTitle(title)


            // let timer = setInterval(async ()=>{
            //     i=i+1
                
            //     if(i>10){
            //         clearTimeout(timer)
            //         console.log('clear')
            //     }
            //     //받아온 정보로 state를 지속적으로 업데이트 하기
        
            // },200)    
        }


        //socket 사용하는 부분
        useEffect( ()=>{

            async function fetchData() {
                let my_url='https://jsonplaceholder.typicode.com/todos/'
                let response = await axios.get(my_url)
                console.log(response.data)
            }

            fetchData()
        },[])
            
            // //소켓 주소 맞게 입력해주세요
            // const socket = io.connect('http://13.124.209.232:5000')
            // console.log(socket)

            // //------소켓이 연결이 안된 상태에서 아래를 활성화 하면 앱이 멈춥니다------
            // socket.on('odom',(data)=>{
            //     let msg = '테스트 성공'+data
            //     setTitle(msg)
            // })

            // const webSocketUrl = `ws://websocket.com`;
            // let ws = new WebSocket(webSocketUrl);
            // ws.onopen = () => {
            //     console.log("connected to " + webSocketUrl);
            // }

        // },[])
        
        return(
            <div>
                {console.log('render')}
                <div className='home-background'>
                    socketio test 입니다
                    <br></br><br></br><br></br>
                    
                    {title}

                    
                    {article}
                    <br></br><br></br><br></br>
                    {/* {title} */}
                    <Navigation onChange={function(idx){
                        console.log('this is onChange function',idx)
                        if(idx=='plus'){
                            setArticle(<New />)
                        }
                        else if (idx=='search'){
                            setArticle(<Search />)
                        }
                        else if (idx=='home_button'){
                            setArticle(<Home />)
                        }
                        else if (idx=='noti'){
                            setArticle(<Notification />)
                        }
                        else if (idx=='profile'){
                            setArticle(<Profile />)
                        }
                        else{
                            setArticle(<Homelogo />)
                        }
                        
                        // let i = 0
                        // getapi(i)



                    } }></Navigation>
                </div>

			
		    </div>

        );
    

}

export default Start;