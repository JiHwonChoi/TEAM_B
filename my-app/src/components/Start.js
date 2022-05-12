import React, {useState, useEffect, useContext} from 'react'
import './start.css'
import New from './New';
import Homelogo from './Homelogo';
import Search from './Search';
import Home from './Home';
import Notification from './Notification';
import Profile from './Profile';
import Navigation from './Navigation';
import Walking from './Walking';
import axios from 'axios';
import socketio from 'socket.io-client'
import { SocketContext } from "../service/socket";






function Start (props) {
        
        const [article, setArticle] = useState(<Homelogo />)
        const [imgurl, setImgurl] = useState('')
        const socket = useContext(SocketContext);
        

        // const socket = socketio.connect('http://127.0.0.1:5000')
        //socket 사용하는 부분
        // useEffect( ()=>{
            
        //     //소켓 주소 맞게 입력해주세요
        //     //------소켓이 연결이 안된 상태에서 아래를 활성화 하면 앱이 멈춥니다------
        //     socket.on('connect', function() {
        //         console.log("socket server connected.");
        //     })
        //     }, [])

        //     socket.on('state', (msg) => {
        //         console.log('received')
        //         console.log(msg)
        //         var arrayBufferView = new Uint8Array( msg.map );
        //         var blob = new Blob( [ arrayBufferView ], { type: "image/jpeg" } );
        //         var urlCreator = window.URL || window.webkitURL;
        //         var imageUrl = urlCreator.createObjectURL( blob );
        //         console.log('imageurl here:', imageUrl)
        //         imageSet(imageUrl)
                
        //     })

        // function showLocation (){
        //     socket.emit( 'robot location')
        // }
        // function imageSet (imageUrl){
        //     setImgurl(imageUrl)
        // }

        function callWalkpath (){
            setArticle(<Walking></Walking>)
        }

        function nav_page_change(idx){
            if(idx=='plus'){
                setArticle(<New pageshift={
                    callWalkpath
                } />)
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
        }
    

        return(
            <div>
                {console.log('render')}
                <div className='home-background'>
                    
                    {article}
                    <br></br><br></br><br></br>
                    {/* <img src={imgurl}></img> */}
                    {/* {title} */}
                    <Navigation onChange={function(idx){
                        console.log('this is onChange function',idx)
                        nav_page_change(idx)
                    } }></Navigation>
                </div>

			
		    </div>

        );
    

}

export default Start;