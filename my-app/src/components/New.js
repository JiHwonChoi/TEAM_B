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
        })

        return () => {
            socket.off('state', (msg) => {
                handlestate(msg)
            })
           
        }
    }, [])

    

    const handlestate  = (msg) => {
        console.log(msg)
        var arrayBufferView = new Uint8Array( msg.map );
        var blob = new Blob( [ arrayBufferView ], { type: "image/jpeg" } );
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL( blob );
        // console.log('imageurl here:', imageUrl)
        setImgurl(imageUrl)
    }

    return (
        <div>
            <div className='title'>
                <div className='big_title'>로봇 역할 카테고리</div>
                <div className='small_title'>원하시는 카테고리를 선택해주세요</div>
            </div>
            <div className='search_tab'>
                    search tab
                </div>

            <div className='robot_current'>
                <img src ={imgurl}></img>
            </div>
            <div className='detail'>산책하기</div>
            <div className='to_my_location'>내 위치로 부르기</div>
            <div className='take_stroll'></div>

        </div>
    )
}

export default New;