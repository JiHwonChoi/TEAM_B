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
import socketio from 'socket.io-client'





function Start (props) {
        
        const [article, setArticle] = useState(<Homelogo />)
        const [title, setTitle] = useState('소켓통신 실패')
        
        //api 지속적으로 새로고침 하는 함수 
        //socket 안되면 이걸로라도
        
        // async function getapi (){
        //     let my_url='http://127.0.0.1:5000/robot_state'
        //         let response = axios.get(my_url)
        //         console.log(response)
        //         let title = response
        //         setTitle(title)
            // let timer = setInterval(async ()=>{
            //     i=i+1
            //     let my_url='https://jsonplaceholder.typicode.com/todos/'+i
            //     let response = await axios.get(my_url)
            //     console.log(response.data)
            //     let title = response.data.title
            //     setTitle(title)
            //     if(i>10){
            //         clearTimeout(timer)
            //         console.log('clear')
            //     }
            //     //받아온 정보로 state를 지속적으로 업데이트 하기
        
            // },200)    
        // }

        const socket = socketio.connect('http://127.0.0.1:5000')

        //socket 사용하는 부분
        useEffect(async ()=>{
            
            //소켓 주소 맞게 입력해주세요
            

            //------소켓이 연결이 안된 상태에서 아래를 활성화 하면 앱이 멈춥니다------
            socket.on('connect', function() {
                
                socket.emit( 'my event', {
                  data: 'User Connected'
                })
            })
            })

            socket.on('server response', function(msg){
                console.log(msg)
            })
        
        // useEffect( ()=>{
        //     console.log("hello")
        //     async function fetchData() {
        //         let my_url='http://127.0.0.1:5000/robot_state'
        //         let response = await axios.get(my_url)
        //         console.log(response.data)
        //     }

        //     fetchData()
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
                        // getapi()



                    } }></Navigation>
                </div>

			
		    </div>

        );
    

}

export default Start;