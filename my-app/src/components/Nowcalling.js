import React, {useState, useEffect, useContext} from 'react'
import './new.css'
import { SocketContext } from "../service/socket";


function Nowcalling(props) {

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
                <div className='big_title'>로봇 호출중 입니다.</div>
                <div className='small_title'>로봇 호출중 입니다.</div>
            </div>
            <div className='search_tab'>
                    search tab
                </div>

            <div className='robot_current'>
                <img src ={imgurl}></img>
            </div>
            <div className='detail' onClick={props.pageshift} >산책하기</div>
            <div className='to_my_location'>취소하기</div>
            <div className='take_stroll'></div>

        </div>
    )
}

export default Nowcalling;