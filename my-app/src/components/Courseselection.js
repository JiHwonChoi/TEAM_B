import React, {useState, useEffect, useContext} from 'react'
import './new.css'
import { SocketContext } from "../service/socket";


function CourseSelection(props) {

    const [imgurl, setImgurl] = useState('')
    const socket = useContext(SocketContext);
    const [popup, setPopup] = useState('')
    
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

    function showpopup (){
        setPopup(<div className='search_popup'> hello </div>)
    }

    return (
        <div>
            course selection page
            <div className='title'>
                <div className='big_title'>로봇 선택</div>
                <div className='small_title'>사용할 로봇을 확인해주세요</div>
            </div>
            <div className='search_tab' onClick = {showpopup}>
                    1층 1호기
                </div>
            {popup}

            <div className='robot_current'>
                <img src ={imgurl}></img>
            </div>
            <div className='detail' onClick={props.pageshift} >산책하기</div>
            <div className='to_my_location'>내 위치로 부르기</div>
            

        </div>
    )
}

export default CourseSelection;