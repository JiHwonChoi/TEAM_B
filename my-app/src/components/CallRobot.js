import React, {useState, useContext} from 'react'
import Navigation from './Navigation';
import './walking.css';
import { SocketContext } from "../service/socket";


function Callrobot (props) {

        const[left,setLeft] = useState(0)
        const[location, setLocation] = useState('101호 로 호출하기')
        const[xclick, setx] = useState(99)
        const[yclick, sety] = useState(71)
        const[roomidx, setroomidx] = useState(0)
        const socket = useContext(SocketContext);

        function goleft(){
            let left_margin = left
            left_margin+=327
            if (left_margin>327){
                left_margin = 0
            }

            setLeft(-1 * left_margin)

        } 

        function goright(){
            let left_margin = left
            left_margin+=327
            if(left_margin>327){
                left_margin=327
            }

            setLeft(-1 * left_margin)
            console.log(left)
            
        }

        function imgClick(e){

            setx(e.nativeEvent.offsetX-12)
            sety(e.nativeEvent.offsetY-20)
            roomWhere(e.nativeEvent.offsetX-12,e.nativeEvent.offsetY-20)
            // this.setState(
            //     {
            //         clicked:{x:e.nativeEvent.offsetX, y: e.nativeEvent.offsetY},
            //         where:{left:(e.pageX-25) +'px',top: (e.pageY-50) +'px' }
            //     }
            // )
       }

       function roomWhere(x,y){
           if(80<x && x<120 && 60<y && y<80){
               setLocation('101호 로 호출하기')
               setroomidx(1)
           }
           else if(187<x && x<220 && 58<y && y<85){
            setLocation('102호 로 호출하기')
            setroomidx(1)
            }
            else if(187<x && x<215 && 130<y && y<280){
                setLocation('103호 로 호출하기')
                setroomidx(1)
                }
            else if(134<x && x<217 && 295<y && y<330){
                setLocation('104호 로 호출하기')
                setroomidx(1)
                }
            else if(80<x && x<114 && 290<y && y<329){
                setLocation('105호 로 호출하기')
                setroomidx(1)
                }
            else if(80<x && x<115 && 213<y && y<282){
                setLocation('106호 로 호출하기')
                setroomidx(1)
                }
            else if(80<x && x<115 && 136<y && y<210){
                setLocation('107호 로 호출하기')
                setroomidx(1)
                }
            else if(124<x && x<173 && 83<y && y<137){
                setLocation('로비로 호출하기')
                setroomidx(1)
                }
           else{
               setLocation('이 위치로는 호출할 수 없습니다')
           }
           
       }

       function gowalk(){

        fetch("http://52.79.237.147:5000/call_sebot",{
            method: "POST",
            headers:{
                "Content-Type":"application/json",
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify({idx: 1})
        }).then((res)=>{
            console.log(res)
            socket.emit('walksign', {'roomidx': roomidx})
            props.gocall()
        })
        console.log('fetch')

        console.log('gowalk')
       }

       
        

        return(
            <div>
                callrobot.js
			<div className='title'>
                <div className='big_title'>로봇 호출 위치 선택</div>
                <div className='small_title'>{location}</div>
            </div>

            <div className='slidewrap'>
                <img className='marker' src='marker.png' style={{left:xclick+'px', top:yclick+'px'}}></img>
                <div className='slide' style={{left:left+'px'}} onClick={imgClick}>
                    <img src='mapimg/testmap.jpg'></img>
                    <img src='mapimg/map.png'></img>
                </div>
                
            </div>
            {/* <div className='map_navigate_wrapper'>
                <div className='buttonWrapper' >
                    <div onClick={goleft}> &lt; 이전</div>
                    <div onClick={goright}> 다음 &gt; </div>
                </div>
            </div> */}
            <div> clicked! x:{xclick} y:{yclick}</div>
            <div className='letsgowalk' onClick={gowalk}>
                <span>산책 시작하기</span></div>
		    </div>

        );
    }


export default Callrobot;