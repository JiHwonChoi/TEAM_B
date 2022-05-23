import React, {useState, useEffect, useContext} from 'react'
// import './new.css'
import { SocketContext } from "../service/socket";


function Walking(props) {

    const [imgurl, setImgurl] = useState('')
    const socket = useContext(SocketContext);
    const [check, setCheck] = useState('재개하기 버튼을 눌러주세요')
    const [pButton, setPButton] = useState(
        {'backgroundColor':'white'}
    )
    const [isPaused, setPaused] = useState(0)

    function press_pause(){
        if(isPaused===0){
            setPButton(
                {'backgroundColor':'grey'},
            )
            setPaused(1)
        }
        else{
            setPButton(
                {'backgroundColor':'white'},
            )
            setPaused(0)
        }
    }


    return (
        <div className='walking_page' style={pButton}>
            this is Walking.js
            <div className='title'>
                <div className='big_title onwalk_1'>일시 정지</div>
                <div className='small_title onwalk_2'>{check}</div>
            </div>

            <div className='detail pause_button' onClick={press_pause} style={pButton} >일시정지</div>
            <div className='to_my_location continue_button' onClick ={press_pause}>재개하기</div>
            <div className='take_stroll'></div>

        </div>
    )
}

export default Walking;