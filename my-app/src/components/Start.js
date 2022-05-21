import React, {useState, useEffect, useContext} from 'react'
import './start.css'
import CourseSelection from './Courseselection';
import Homelogo from './Homelogo';
import Search from './Search';
import Home from './Home';
import Notification from './Notification';
import Profile from './Profile';
import Navigation from './Navigation';
import Walking from './Walking';
import Nowcalling from './Nowcalling';
import Callrobot from './CallRobot';
import axios from 'axios';
import socketio from 'socket.io-client'
import { SocketContext } from "../service/socket";






function Start (props) {
        
        const [article, setArticle] = useState(<Homelogo />)
        const [imgurl, setImgurl] = useState('')
        const socket = useContext(SocketContext);
        
        function callWalkpage (){
            setArticle(<Walking />)
        }

        function callrobot (){
            setArticle(<Callrobot gocall={
                callNowcalling
            }></Callrobot>)
        }

        function callNowcalling(){
            console.log('hey')
            setArticle(<Nowcalling gowalk={callWalkpage}></Nowcalling>)
        }

        function callNewpage(){
            setArticle(<CourseSelection pageshift={
                callrobot
            } />)
        }

        function nav_page_change(idx){
            if(idx=='plus'){
                setArticle(<CourseSelection pageshift={
                    callrobot
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
                    
                    <Navigation onChange={function(idx){
                        console.log('this is onChange function',idx)
                        nav_page_change(idx)
                    } }></Navigation>
                </div>

			
		    </div>

        );
    

}

export default Start;