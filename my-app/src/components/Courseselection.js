import React, {useState, useEffect, useContext} from 'react'
import './new.css'
import { SocketContext } from "../service/socket";


function New(props) {

    const [imgurl, setImgurl] = useState('')
    const socket = useContext(SocketContext);
    
    useEffect( ()=>{
        socket.emit( 'robot location')
        console.log('!!!request location!!!')
        socket.on('state', (msg) => {
                handlestate(msg)
                socket.off('state')
        })

        return () => {
            socket.off('state')
           
        }
    }, [])

    

    const handlestate  = (msg) => {
        // console.log(msg)
        var arrayBufferView = new Uint8Array( msg.map );
        var blob = new Blob( [ arrayBufferView ], { type: "image/jpeg" } );
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL( blob );
        console.log('imageurl here:', imageUrl)
        setImgurl(imageUrl)
    }

    return (
        <div>
            course selection page
            <div className='title'>
                <div className='big_title'>코스 선택</div>
                <div className='small_title'>산책할 코스를 선택해주세요</div>
            </div>
            <div className='search_tab'>
                    1층 1호기
                </div>

            <div className='robot_current'>
                <img src ={imgurl}></img>
            </div>
            <div className='detail' onClick={props.pageshift} >산책하기</div>
            <div className='to_my_location'>내 위치로 부르기</div>
            <div className='take_stroll'></div>

        </div>
    )
}

export default New;