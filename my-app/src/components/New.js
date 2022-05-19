import React, {useState, useEffect, useContext} from 'react'
import './new.css'
import { SocketContext } from "../service/socket";
import axios from 'axios';


function New(props) {

    const [imgurl, setImgurl] = useState('')
    const socket = useContext(SocketContext);
    
    useEffect( ()=>{
        socket.emit( 'robot location')
        console.log('!!!request location!!!')
    }, [])

    socket.on('state', (msg) => {
        // console.log('received')
        console.log(msg)
        var arrayBufferView = new Uint8Array( msg.map );
        var blob = new Blob( [ arrayBufferView ], { type: "image/jpeg" } );
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL( blob );
        // console.log('imageurl here:', imageUrl)
        console.log(imageUrl)
        console.log(typeof(imageUrl))

        setImgurl(imageUrl)
        
    })

    return (
        <div>
            <p>This is new page</p>
            <div className='title'>
                <div className='big_title'>로봇 역할 카테고리</div>
                <div className='small_title'>원하시는 카테고리를 선택해주세요</div>
            </div>
            <div className='search_tab'>
                    search tab
                </div>

            <div className='robot_current'>
                로봇의 현재 위치 표시
                <img src ={imgurl}></img>
            </div>
            <div className='detail'>goto detail page</div>
            <div className='to_my_location'>goto mylocation page</div>
            <div className='take_stroll'></div>

        </div>
    )
}

export default New;