import React, {useState, useEffect, useContext} from 'react'
import './new.css'
import { SocketContext } from "../service/socket";


function Nowcalling(props) {

    const [imgurl, setImgurl] = useState('')
    const socket = useContext(SocketContext);
    const [buttonColor, setButtonColor] = useState(
        {'backgroundColor':'lightgrey'}
    )
    const [arrived, setArrived] = useState('0')

    // setTimeout(robotArrival,3000)

    useEffect( ()=>{
        socket.emit( 'robot location')
        console.log('!!!request location!!!')
        socket.on('state', (msg) => {
            console.log(msg.arrival)
            if(msg.arrival){
                socket.off('state')
                alert('!도착!')
                robotArrival()
                
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

    function robotArrival(){
        setButtonColor({'backgroundColor':'lightgreen'})
        setArrived(1)
        
    }

    function checkarrive(){
        
        if(arrived==1){
            console.log('hey')
             return props.gowalk()
        }

        else return

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
            this is Nowcalling.js
            <div className='title'>
                <div className='big_title'>로봇 호출중 입니다.</div>
                <div className='small_title'>로봇 호출중 입니다.</div>
            </div>
            <div className='search_tab'>
                    1층 1호기
                </div>

            <div className='robot_current'>
                <img src ={imgurl}></img>
            </div>
            <div className='detail' onClick={checkarrive} style={buttonColor} >산책하기</div>
            <div className='to_my_location' onClick ={props.canceled}>취소하기</div>
            <div className='take_stroll'></div>

        </div>
    )
}

export default Nowcalling;