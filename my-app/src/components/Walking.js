import React, {useState, useEffect, useContext} from 'react'
// import './new.css'
import { SocketContext } from "../service/socket";


function Walking(props) {

    const [imgurl, setImgurl] = useState('')
    const socket = useContext(SocketContext);
    const [check, setCheck] = useState('1호기 이용중 입니다.')

    setTimeout(finishWalking, 2000)
    
    useEffect( ()=>{
        socket.emit( 'robot location')
        console.log('!!!request location!!!')
        socket.on('state', (msg) => {
            console.log(msg.arrival)
            if(msg.arrival){
                socket.off('state')
                finishWalking()
            }
            else{
                handlestate(msg)
            }
        })

        return () => {
            socket.off('state', (msg) => {
                handlestate(msg)
            })
           
        }
    }, [])

    function finishWalking(){

        setCheck('산책을 완료하였습니다.')

    }

    const handlestate  = (msg) => {
        // console.log(msg)
        var arrayBufferView = new Uint8Array( msg.map );
        var blob = new Blob( [ arrayBufferView ], { type: "image/jpeg" } );
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL( blob );
        // console.log('imageurl here:', imageUrl)
        setImgurl(imageUrl)
        socket.emit( 'robot location')

    }

    return (
        <div>
            this is Walking.js
            <div className='title'>
                <div className='big_title'>산책 중 입니다.</div>
                <div className='small_title'>{check}</div>
            </div>

            <div className='robot_current_walking'>
                <img src ={imgurl}></img>
            </div>
            <div className='detail' onClick={props.gowalk} >응급호출</div>
            <div className='to_my_location' onClick ={props.canceled}>취소하기</div>
            <div className='take_stroll'></div>

        </div>
    )
}

export default Walking;